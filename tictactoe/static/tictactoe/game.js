const TicTacToe = {
    apiBaseUrl: '/tictactoe/api',
    currentGameId: null,

    getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    },

    async createGame() {
        try {
            const csrfToken = this.getCsrfToken();
            const headers = {
                'Content-Type': 'application/json',
            };

            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
            }

            const response = await fetch(`${this.apiBaseUrl}/games/`, {
                method: 'POST',
                headers: headers,
            });

            if (response.ok) {
                const data = await response.json();
                return data.id;
            } else {
                const errorData = await response.json().catch(() => ({}));
                this.showError(errorData.detail || 'Failed to create game');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    },

    async loadGame(gameId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${gameId}/`);

            if (response.ok) {
                const data = await response.json();
                this.updateBoard(data);
                return data;
            } else {
                this.showError('Failed to load game');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    },

    async makeMove(gameId, position) {
        try {
            const csrfToken = this.getCsrfToken();
            const headers = {
                'Content-Type': 'application/json',
            };

            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
            }

            const response = await fetch(`${this.apiBaseUrl}/games/${gameId}/move/`, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ position }),
            });

            const data = await response.json();

            if (response.ok) {
                this.updateBoard(data);
                this.showMessage(data.message || 'Move successful', 'success');
                return data;
            } else {
                this.showError(data.error || 'Invalid move');
                return null;
            }
        } catch (error) {
            this.showError('Network error: ' + error.message);
            return null;
        }
    },

    updateBoard(gameData) {
        // Update board cells
        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell, index) => {
            const mark = gameData.board[index];
            cell.innerHTML = mark ? `<span class="mark mark-${mark}">${mark}</span>` : '';

            // Enable/disable cells based on game state
            if (gameData.status === 'in_progress' && !mark) {
                cell.classList.add('clickable');
            } else {
                cell.classList.remove('clickable');
            }
        });

        // Update game info
        const currentPlayerEl = document.getElementById('current-player');
        if (currentPlayerEl) {
            currentPlayerEl.textContent = gameData.current_player;
            currentPlayerEl.className = `value player-${gameData.current_player}`;
        }

        const statusEl = document.getElementById('game-status');
        if (statusEl) {
            const statusText = {
                'in_progress': 'In Progress',
                'x_wins': 'X Wins!',
                'o_wins': 'O Wins!',
                'draw': 'Draw'
            }[gameData.status];
            statusEl.textContent = statusText;
            statusEl.className = `value status-${gameData.status}`;
        }

        // Show game over message
        if (gameData.status !== 'in_progress') {
            const messages = {
                'x_wins': '🎉 Player X wins!',
                'o_wins': '🎉 Player O wins!',
                'draw': '🤝 It\'s a draw!'
            };
            this.showMessage(messages[gameData.status], 'success');
        }
    },

    showMessage(text, type = 'info') {
        const messageEl = document.getElementById('message');
        if (messageEl) {
            messageEl.textContent = text;
            messageEl.className = `message message-${type}`;
            setTimeout(() => {
                messageEl.textContent = '';
                messageEl.className = 'message';
            }, 3000);
        }
    },

    showError(text) {
        this.showMessage(text, 'error');
    },

    initGame(gameId) {
        this.currentGameId = gameId;

        // Load initial game state
        this.loadGame(gameId);

        // Setup cell click handlers
        const board = document.getElementById('game-board');
        if (board) {
            board.addEventListener('click', async (e) => {
                const cell = e.target.closest('.cell');
                if (cell && cell.classList.contains('clickable')) {
                    const position = parseInt(cell.dataset.position);
                    await this.makeMove(gameId, position);
                }
            });
        }

        // Setup new game button
        const newGameBtn = document.getElementById('new-game-btn');
        if (newGameBtn) {
            newGameBtn.addEventListener('click', async () => {
                const newGameId = await this.createGame();
                if (newGameId) {
                    window.location.href = `/tictactoe/game/${newGameId}/`;
                }
            });
        }

        // Setup refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadGame(gameId);
            });
        }
    }
};
