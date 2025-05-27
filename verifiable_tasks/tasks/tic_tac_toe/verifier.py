import re
import json
import copy
import time
import signal
import re
import ast
def extract_json_code(text):
    """
    Extract JSON code blocks from the given text.
    """
    pattern = r'```json(.*?)```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks

def check_winner(board, win_length=None):
    """
    Check if any player (X or O) has formed a line of win_length on the current board. Return None if not.
    Supports boards of any size.
    """
    size = len(board)
    if win_length is None:
        win_length = size  # Default win length equals board size
    
    # Check rows
    for i in range(size):
        for j in range(size - win_length + 1):
            if board[i][j] != "" and all(board[i][j] == board[i][j+k] for k in range(win_length)):
                return board[i][j]
    
    # Check columns
    for i in range(size - win_length + 1):
        for j in range(size):
            if board[i][j] != "" and all(board[i][j] == board[i+k][j] for k in range(win_length)):
                return board[i][j]
    
    # Check main diagonals
    for i in range(size - win_length + 1):
        for j in range(size - win_length + 1):
            if board[i][j] != "" and all(board[i+k][j+k] == board[i][j] for k in range(win_length)):
                return board[i][j]
    
    # Check anti-diagonals
    for i in range(size - win_length + 1):
        for j in range(win_length - 1, size):
            if board[i][j] != "" and all(board[i+k][j-k] == board[i][j] for k in range(win_length)):
                return board[i][j]
    
    return None

def is_full(board):
    """Check if the board is full"""
    return all(cell != "" for row in board for cell in row)

def opponent(player):
    """Return the opponent's piece type"""
    return 'O' if player == 'X' else 'X'

def evaluate_board(board, player, win_length=None):
    """
    Heuristic evaluation function to assess how favorable the board is for player
    Returns a score between [-1, 1]
    """
    size = len(board)
    if win_length is None:
        win_length = size
    
    # Check if there's a winner
    winner = check_winner(board, win_length)
    if winner == player:
        return 1
    elif winner == opponent(player):
        return -1
    
    # If no winner, evaluate potential line possibilities
    score = 0
    
    # Evaluation function: count potential lines for player and opponent
    player_potential = count_potential_lines(board, player, win_length)
    opponent_potential = count_potential_lines(board, opponent(player), win_length)
    
    # Normalize to [-0.9, 0.9] range
    if player_potential + opponent_potential > 0:
        score = 0.9 * (player_potential - opponent_potential) / (player_potential + opponent_potential)
    
    return score

def improved_evaluate_board(board, player, win_length=None):
    """
    Improved evaluation function for more accurate board state assessment
    """
    size = len(board)
    if win_length is None:
        win_length = size
    
    # Check if there's a winner
    winner = check_winner(board, win_length)
    if winner == player:
        return 1
    elif winner == opponent(player):
        return -1
    
    # Base score: potential lines
    player_potential = count_potential_lines(board, player, win_length)
    opponent_potential = count_potential_lines(board, opponent(player), win_length)
    
    # Additional score: center control
    center_score = 0
    center = size // 2
    center_positions = []
    
    # Define center area
    if size % 2 == 1:  # Odd-sized board
        center_positions = [(center, center)]
        if size > 3:
            for i in range(center-1, center+2):
                for j in range(center-1, center+2):
                    if (i, j) != (center, center):
                        center_positions.append((i, j))
    else:  # Even-sized board
        center_positions = [(center-1, center-1), (center-1, center), 
                           (center, center-1), (center, center)]
    
    # Calculate center control score
    for i, j in center_positions:
        if board[i][j] == player:
            center_score += 0.1
        elif board[i][j] == opponent(player):
            center_score -= 0.1
    
    # Additional score: forks (multiple threats)
    player_forks = count_forks(board, player, win_length)
    opponent_forks = count_forks(board, opponent(player), win_length)
    fork_score = 0.2 * (player_forks - opponent_forks)
    
    # Combined score, ensuring it's within [-0.99, 0.99] range
    base_score = 0
    if player_potential + opponent_potential > 0:
        base_score = 0.7 * (player_potential - opponent_potential) / (player_potential + opponent_potential)
    
    total_score = base_score + center_score + fork_score
    
    # Limit to reasonable range
    return max(min(total_score, 0.99), -0.99)

def count_forks(board, player, win_length):
    """
    Count the number of "forks" (multiple threats) the player can form
    """
    size = len(board)
    fork_count = 0
    
    # Try placing the player's piece in each empty cell, check if it forms multiple threats
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                board[i][j] = player
                threat_lines = 0
                
                # Check row threats
                for row in range(size):
                    for col in range(size - win_length + 1):
                        line = [board[row][col+k] for k in range(win_length)]
                        empty_count = line.count("")
                        player_count = line.count(player)
                        if empty_count == 1 and player_count == win_length - 1:
                            threat_lines += 1
                
                # Check column threats
                for col in range(size):
                    for row in range(size - win_length + 1):
                        line = [board[row+k][col] for k in range(win_length)]
                        empty_count = line.count("")
                        player_count = line.count(player)
                        if empty_count == 1 and player_count == win_length - 1:
                            threat_lines += 1
                
                # Check main diagonal threats
                for row in range(size - win_length + 1):
                    for col in range(size - win_length + 1):
                        line = [board[row+k][col+k] for k in range(win_length)]
                        empty_count = line.count("")
                        player_count = line.count(player)
                        if empty_count == 1 and player_count == win_length - 1:
                            threat_lines += 1
                
                # Check anti-diagonal threats
                for row in range(size - win_length + 1):
                    for col in range(win_length - 1, size):
                        line = [board[row+k][col-k] for k in range(win_length)]
                        empty_count = line.count("")
                        player_count = line.count(player)
                        if empty_count == 1 and player_count == win_length - 1:
                            threat_lines += 1
                
                # If there are multiple threat lines, count as one fork
                if threat_lines >= 2:
                    fork_count += 1
                
                board[i][j] = ""  # Restore the board
    
    return fork_count

def count_potential_lines(board, player, win_length):
    """
    Count the number of potential lines the player can form on the board
    Potential lines: current pieces of player and empty cells (can be formed in the future)
    """
    size = len(board)
    potential_count = 0
    
    # Check rows
    for i in range(size):
        for j in range(size - win_length + 1):
            line = [board[i][j+k] for k in range(win_length)]
            if opponent(player) not in line and player in line:
                # The row has no opponent's pieces and has player's pieces
                potential_count += 1
    
    # Check columns
    for i in range(size - win_length + 1):
        for j in range(size):
            line = [board[i+k][j] for k in range(win_length)]
            if opponent(player) not in line and player in line:
                potential_count += 1
    
    # Check main diagonals
    for i in range(size - win_length + 1):
        for j in range(size - win_length + 1):
            line = [board[i+k][j+k] for k in range(win_length)]
            if opponent(player) not in line and player in line:
                potential_count += 1
    
    # Check anti-diagonals
    for i in range(size - win_length + 1):
        for j in range(win_length - 1, size):
            line = [board[i+k][j-k] for k in range(win_length)]
            if opponent(player) not in line and player in line:
                potential_count += 1
    
    return potential_count

def minimax_alpha_beta(board, current_turn, maximizing_player, depth=0, max_depth=5, alpha=-float('inf'), beta=float('inf'), win_length=None):
    """
    Minimax algorithm with Alpha-Beta pruning to evaluate board state
    """
    size = len(board)
    if win_length is None:
        win_length = size
    
    # Check termination conditions
    winner = check_winner(board, win_length)
    if winner is not None:
        return 1 if winner == maximizing_player else -1
    
    if is_full(board):
        return 0
    
    # Use heuristic evaluation at max depth
    if depth >= max_depth:
        return improved_evaluate_board(board, maximizing_player, win_length)
    
    # Get all possible moves
    moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                moves.append((i, j))
    
    # Sort moves for better Alpha-Beta pruning efficiency
    if depth == 0:
        # At top level, prioritize center and corner positions
        center = size // 2
        moves.sort(key=lambda m: -1 if (m[0] == center and m[1] == center) or 
                                      (m[0] in [0, size-1] and m[1] in [0, size-1]) else 0)
    
    if current_turn == maximizing_player:
        max_eval = -float('inf')
        for i, j in moves:
            board[i][j] = current_turn
            eval = minimax_alpha_beta(board, opponent(current_turn), maximizing_player, 
                                     depth+1, max_depth, alpha, beta, win_length)
            board[i][j] = ""
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta pruning
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in moves:
            board[i][j] = current_turn
            eval = minimax_alpha_beta(board, opponent(current_turn), maximizing_player, 
                                     depth+1, max_depth, alpha, beta, win_length)
            board[i][j] = ""
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha pruning
        return min_eval

def minimax_complete(board, current_player, maximizing_player, is_maximizing, win_length=3):
    """
    Complete minimax algorithm, no depth limit, suitable for 3x3 board
    """
    # Check if there's a winner
    winner = check_winner(board, win_length)
    if winner == maximizing_player:
        return 1
    elif winner and winner != maximizing_player:
        return -1
    elif is_full(board):
        return 0
    
    size = len(board)
    if is_maximizing:
        best_score = -float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == "":
                    board[i][j] = current_player
                    score = minimax_complete(board, opponent(current_player), 
                                           maximizing_player, False, win_length)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == "":
                    board[i][j] = current_player
                    score = minimax_complete(board, opponent(current_player), 
                                           maximizing_player, True, win_length)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def check_immediate_actions(board, player, win_length):
    """
    Check if there's an immediate win or block opponent's win move
    Returns: (whether there's an immediate move, best move list)
    """
    size = len(board)
    board_copy = copy.deepcopy(board)
    opponent_player = opponent(player)
    immediate_moves = []
    
    # Check immediate win
    for i in range(size):
        for j in range(size):
            if board_copy[i][j] == "":
                board_copy[i][j] = player
                if check_winner(board_copy, win_length) == player:
                    immediate_moves.append((i, j))
                board_copy[i][j] = ""
    
    # If there's an immediate win move, return them
    if immediate_moves:
        return (True, immediate_moves)
    
    # Check block opponent's win
    blocking_moves = []
    for i in range(size):
        for j in range(size):
            if board_copy[i][j] == "":
                board_copy[i][j] = opponent_player
                if check_winner(board_copy, win_length) == opponent_player:
                    blocking_moves.append((i, j))
                board_copy[i][j] = ""
    
    # If there's a block opponent's win move, return them
    if blocking_moves:
        return (True, blocking_moves)
    
    # No immediate win or block situation
    return (False, [])

def find_best_move_3x3(board, active_player):
    """
    Complete game tree search for 3x3 board, ensuring optimal solution
    """
    # Check if there's an immediate win or block opponent's win move
    has_immediate, immediate_moves = check_immediate_actions(board, active_player, 3)
    if has_immediate:
        return immediate_moves
    
    best_score = -float('inf')
    best_moves = []
    
    # Complete minimax search, no depth limit
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = active_player
                # Minimax without depth limit
                score = minimax_complete(board, opponent(active_player), active_player, False)
                board[i][j] = ""
                
                if score > best_score:
                    best_score = score
                    best_moves = [(i, j)]
                elif score == best_score:
                    best_moves.append((i, j))
    
    return best_moves

def find_best_move_larger_board(board, active_player, win_length=None, max_time=30):
    """
    Improved search algorithm for larger board, using multi-level search and time limit
    """
    size = len(board)
    if win_length is None:
        win_length = size
    
    # Check if there's an immediate win or block opponent's win move
    has_immediate, immediate_moves = check_immediate_actions(board, active_player, win_length)
    if has_immediate:
        return immediate_moves
    
    empty_count = sum(1 for row in board for cell in row if cell == "")
    
    # Set search depth
    if size == 4:
        if empty_count <= 4:
            max_depths = [16, 12, 8]  # Multi-level search depth
        elif empty_count <= 8:
            max_depths = [10, 8, 6]
        else:
            max_depths = [6, 4, 2]
    else:  # 5x5 or larger
        if empty_count <= 4:
            max_depths = [12, 8, 4]
        elif empty_count <= 8:
            max_depths = [8, 6, 4]
        elif empty_count <= 12:
            max_depths = [6, 4, 2]
        else:
            max_depths = [4, 3, 2]
    
    # Multi-level search result
    all_best_moves = []
    start_time = time.time()
    
    # Search from shallow to deep step by step until time runs out
    for depth_index, max_depth in enumerate(max_depths):
        # Check if there's enough time for next level search
        current_time = time.time()
        if current_time - start_time > max_time:
            break
        
        best_score = -float('inf')
        best_moves = []
        
        # Use Alpha-Beta search to evaluate all moves
        for i in range(size):
            for j in range(size):
                if board[i][j] == "":
                    # Check if time runs out
                    if time.time() - start_time > max_time:
                        break
                    
                    board[i][j] = active_player
                    # Use Alpha-Beta pruning Minimax algorithm
                    score = minimax_alpha_beta(board, opponent(active_player), active_player, 
                                             0, max_depth, -float('inf'), float('inf'), win_length)
                    board[i][j] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_moves = [(i, j)]
                    elif score == best_score:
                        best_moves.append((i, j))
            
            # Check if time runs out
            if time.time() - start_time > max_time:
                break
        
        # Record current depth's best move
        if best_moves:
            all_best_moves.append(best_moves)
    
    # If there's multi-level search result, prioritize the deepest result
    if all_best_moves:
        return all_best_moves[-1]
    
    # If there's no search result (possibly because of time limit), use heuristic evaluation
    best_score = -float('inf')
    best_moves = []
    
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                board[i][j] = active_player
                score = improved_evaluate_board(board, active_player, win_length)
                board[i][j] = ""
                
                if score > best_score:
                    best_score = score
                    best_moves = [(i, j)]
                elif score == best_score:
                    best_moves.append((i, j))
    
    return best_moves

def compare_boards(board1, board2):
    """Compare two boards for equality"""
    if len(board1) != len(board2):
        return False
    
    size = len(board1)
    for i in range(size):
        if len(board1[i]) != len(board2[i]):
            return False
        for j in range(size):
            if board1[i][j] != board2[i][j]:
                return False
    return True

def validate_answer_is_one_move(question, answer, active_player):
    """Validate if the answer is only one move"""
    if len(question) != len(answer):
        return False
    
    size = len(question)
    move_count = 0
    move_position = None
    
    for i in range(size):
        if len(question[i]) != len(answer[i]):
            return False
        for j in range(size):
            # If question already has a piece, answer must be the same
            if question[i][j] != "":
                if question[i][j] != answer[i][j]:
                    return False
            else:
                # Originally empty, answer may fill in active_player, or still be empty
                if answer[i][j] == active_player:
                    move_count += 1
                    move_position = (i, j)
                elif answer[i][j] != "":
                    # Answer fills in an opponent's piece, which is not allowed
                    return False
    
    # Ensure only one move
    if move_count != 1:
        return False
    
    # Ensure move is in valid position
    if move_position is None:
        return False
    
    return True

def find_move_position(original_board, new_board, player):
    """Find the position of the piece added in the new board"""
    size = len(original_board)
    for i in range(size):
        for j in range(size):
            if original_board[i][j] == "" and new_board[i][j] == player:
                return (i, j)
    return None

def extract_last_code_block(text: str):
    code_blocks = re.findall(r'```.*?\n(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    return code_blocks[-1].strip() if code_blocks else None


def parse_answer(answer: str, delimiter: str = None):
    if not answer:
        return None
    rows = answer.split("\n")
    result = []
    
    for row in rows:
        row = row.strip()
        if not row:
            continue
        
        columns = row.split(delimiter) if delimiter else row.split()
        result.append([grid.replace('"','') for grid in columns])
    
    return result if all(None not in row for row in result) else None

def verify_with_timeout(func, *args, timeout=60):
    """Function execution with timeout protection"""
    result = [None]
    
    def handler(signum, frame):
        raise TimeoutError("Function execution timed out")
    
    # Set signal handling
    old_handler = signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    
    try:
        result[0] = func(*args)
    except TimeoutError:
        print("Execution timed out")
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
    
    return result[0]

def parse_list_str(input_string):
    try:
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError):
        return None

def preprocess_answer_to_matrix(raw_answer):
    if isinstance(raw_answer, list):
        return raw_answer
    
    answer = parse_answer(raw_answer, delimiter=None)
    if answer is None:
        answer = parse_answer(raw_answer, delimiter=',')
    if answer is None:
        answer = parse_list_str(raw_answer)
    
    return answer

def verify(pred, answer, meta):
    """
    Validate if the prediction result is correct, supports different board sizes.
    Use improved algorithm for verification, select different verification strategy based on board size.
    """
    try:
        # Start timing
        start_time = time.time()
        
        # answer parameter processing
        if isinstance(answer, str):
            try:
                answer = json.loads(answer)
            except json.JSONDecodeError:
                pass

        # meta can be string or dict
        if isinstance(meta, str):
            try:
                meta = json.loads(meta)
            except json.JSONDecodeError:
                return 0
        
        if not isinstance(meta, dict):
            return 0
        
        # Extract necessary information
        try:
            current_board = meta["current_board"]
            active_player = meta["active_player"]
            
            # Get board size and win length
            board_size = meta.get("board_size", "3x3")
            size = len(current_board)
            
            # Determine win length
            win_length = size  # Default win length equals board size
            if "win_length" in meta:
                win_length = meta["win_length"]
            elif board_size in ["3x3", "4x4", "5x5"]:
                win_length = int(board_size[0])
        except (KeyError, ValueError):
            return 0
        
        pred = extract_last_code_block(pred)
        if pred is None:
            return 0
        pred_answer = preprocess_answer_to_matrix(pred)
        if pred_answer is None:
            return 0
        
        

        # Validate if the answer is only one valid move
        if not validate_answer_is_one_move(current_board, pred_answer, active_player):
            return 0
        
        # Find the predicted move position
        move_position = find_move_position(current_board, pred_answer, active_player)
        if not move_position:
            return 0
        
        # Select different verification algorithm based on board size
        if size == 3:
            # Use complete search for 3x3 (ensure absolute correctness)
            optimal_moves = find_best_move_3x3(current_board, active_player)
            is_valid_answer = move_position in optimal_moves
        else:
            # Check if there's an immediate win or block opponent's win move
            has_immediate, immediate_moves = check_immediate_actions(current_board, active_player, win_length)
            
            if has_immediate:
                # If there's an immediate move, must choose one of them
                is_valid_answer = move_position in immediate_moves
            else:
                # Use multi-level search for larger board
                # Set time limit to avoid too long search time
                remaining_time = max(1, 30 - (time.time() - start_time))
                optimal_moves = find_best_move_larger_board(
                    current_board, active_player, win_length, max_time=remaining_time)
                
                is_valid_answer = move_position in optimal_moves
        
        # Record verification time
        end_time = time.time()
        verification_time = end_time - start_time
        #print(f"Verification completed in {verification_time:.2f} seconds")
        
        return int(is_valid_answer)
    
    except Exception as e:
        print(f"Verification error: {str(e)}")
        return 0
