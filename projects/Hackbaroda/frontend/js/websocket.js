/**
 * ============================================================================
 * Aetheris WebSocket Manager
 * ============================================================================
 * Handles real-time communication with the backend strategy engine.
 *
 * BACKEND TEAM: Update WS_URL below to point at your server endpoint.
 *
 * Message protocol
 * ────────────────
 * All messages are JSON with the shape:  { type: string, payload: object }
 *
 * Inbound types (server → client):
 *   'chat_response'      → onChatResponse(payload)
 *   'artifact_update'    → onArtifactUpdate(payload)
 *   'typing_indicator'   → onTypingIndicator(payload.isTyping)
 *   'session_update'     → onSessionUpdate(payload)
 *
 * Outbound types (client → server):
 *   'onboarding_complete'
 *   'chat_message'
 *   'get_artifacts'
 *   'feedback'
 * ============================================================================
 */

const WS_URL = 'ws://localhost:8080';

class AetherisSocket {
  // ---------------------------------------------------------------------------
  // Construction
  // ---------------------------------------------------------------------------

  /**
   * Create a new AetherisSocket instance.
   * @param {string} url - WebSocket server URL.
   */
  constructor(url = WS_URL) {
    /** @private */ this._url = url;
    /** @private */ this._ws = null;

    /** Whether the socket is currently connected. */
    this.isConnected = false;

    /** @private */ this._reconnectAttempts = 0;
    /** @private */ this._maxReconnectAttempts = 10;
    /** @private */ this._reconnectTimer = null;

    /**
     * Messages queued while the socket is disconnected.
     * They are flushed automatically once the connection is re-established.
     * @private
     * @type {Array<string>}
     */
    this._messageQueue = [];

    // ── Event handler slots (override from app.js) ──────────────────────

    /** Called when the WebSocket connection opens. */
    this.onConnect = () => {};

    /** Called when the WebSocket connection closes. */
    this.onDisconnect = () => {};

    /**
     * Called when a connection error occurs.
     * @param {Event} error
     */
    this.onError = (error) => {};

    /**
     * Called when an AI chat response is received.
     * @param {object} data - The response payload.
     */
    this.onChatResponse = (data) => {};

    /**
     * Called when the artifact list is updated.
     * @param {object} data - The artifact payload.
     */
    this.onArtifactUpdate = (data) => {};

    /**
     * Called when the AI typing indicator state changes.
     * @param {boolean} isTyping
     */
    this.onTypingIndicator = (isTyping) => {};

    /**
     * Called on session or auth state updates.
     * @param {object} data - The session payload.
     */
    this.onSessionUpdate = (data) => {};
  }

  // ---------------------------------------------------------------------------
  // Connection Lifecycle
  // ---------------------------------------------------------------------------

  /**
   * Open a WebSocket connection to the configured URL.
   * Automatically reconnects on unexpected disconnects.
   */
  connect() {
    // Prevent duplicate connections.
    if (this._ws && (this._ws.readyState === WebSocket.OPEN || this._ws.readyState === WebSocket.CONNECTING)) {
      console.warn('[AetherisSocket] Connection already open or in progress — skipping.');
      return;
    }

    console.log(`[AetherisSocket] Connecting to ${this._url}…`);

    try {
      this._ws = new WebSocket(this._url);
    } catch (err) {
      console.error('[AetherisSocket] Failed to create WebSocket:', err);
      this._reconnect();
      return;
    }

    // ── onopen ──────────────────────────────────────────────────────────
    this._ws.onopen = () => {
      console.log('[AetherisSocket] Connected ✓');
      this.isConnected = true;
      this._reconnectAttempts = 0;
      this.onConnect();
      this._flushQueue();
    };

    // ── onclose ─────────────────────────────────────────────────────────
    this._ws.onclose = (event) => {
      console.log(`[AetherisSocket] Disconnected (code ${event.code}, reason: "${event.reason || 'none'}")`);
      this.isConnected = false;
      this.onDisconnect();

      // Only auto-reconnect for abnormal closures (not manual disconnect).
      if (event.code !== 1000) {
        this._reconnect();
      }
    };

    // ── onerror ─────────────────────────────────────────────────────────
    this._ws.onerror = (error) => {
      console.error('[AetherisSocket] Connection error:', error);
      this.onError(error);
      // The browser will fire `onclose` immediately after `onerror`, which
      // triggers the reconnect path — no need to call _reconnect() here.
    };

    // ── onmessage ───────────────────────────────────────────────────────
    this._ws.onmessage = (event) => {
      this._handleMessage(event);
    };
  }

  /**
   * Gracefully close the WebSocket connection.
   * Clears any pending reconnect timer.
   */
  disconnect() {
    console.log('[AetherisSocket] Disconnecting…');

    // Cancel any queued reconnect.
    if (this._reconnectTimer) {
      clearTimeout(this._reconnectTimer);
      this._reconnectTimer = null;
    }

    this._reconnectAttempts = 0;

    if (this._ws) {
      this._ws.close(1000, 'Client disconnected');
      this._ws = null;
    }

    this.isConnected = false;
  }

  /**
   * Schedule a reconnection attempt with exponential back-off.
   * Delays: 1 s → 2 s → 4 s → 8 s → … → max 30 s.
   * @private
   */
  _reconnect() {
    if (this._reconnectAttempts >= this._maxReconnectAttempts) {
      console.error(
        `[AetherisSocket] Max reconnect attempts (${this._maxReconnectAttempts}) reached. Giving up.`
      );
      return;
    }

    // Exponential back-off capped at 30 seconds.
    const delay = Math.min(1000 * Math.pow(2, this._reconnectAttempts), 30000);
    this._reconnectAttempts++;

    console.log(
      `[AetherisSocket] Reconnecting in ${delay / 1000}s (attempt ${this._reconnectAttempts}/${this._maxReconnectAttempts})…`
    );

    this._reconnectTimer = setTimeout(() => {
      this.connect();
    }, delay);
  }

  // ---------------------------------------------------------------------------
  // Internal Messaging
  // ---------------------------------------------------------------------------

  /**
   * Serialize a message and send it over the socket.
   * If the socket is not connected the message is queued for later delivery.
   *
   * @private
   * @param {string} type    - Message type identifier.
   * @param {object} payload - Arbitrary data payload.
   */
  _send(type, payload = {}) {
    const message = JSON.stringify({ type, payload });

    if (this.isConnected && this._ws && this._ws.readyState === WebSocket.OPEN) {
      console.log(`[AetherisSocket] Sending → ${type}`, payload);
      this._ws.send(message);
    } else {
      console.warn(`[AetherisSocket] Socket not connected — queuing message: ${type}`);
      this._messageQueue.push(message);
    }
  }

  /**
   * Flush the offline message queue once the connection is restored.
   * @private
   */
  _flushQueue() {
    if (this._messageQueue.length === 0) return;

    console.log(`[AetherisSocket] Flushing ${this._messageQueue.length} queued message(s)…`);

    while (this._messageQueue.length > 0) {
      const message = this._messageQueue.shift();
      if (this._ws && this._ws.readyState === WebSocket.OPEN) {
        this._ws.send(message);
      } else {
        // Put it back if the socket closed between flushes.
        this._messageQueue.unshift(message);
        console.warn('[AetherisSocket] Socket closed during flush — stopping.');
        break;
      }
    }
  }

  /**
   * Parse an incoming WebSocket message and route it to the appropriate handler.
   * @private
   * @param {MessageEvent} event - The raw WebSocket message event.
   */
  _handleMessage(event) {
    let data;

    try {
      data = JSON.parse(event.data);
    } catch (err) {
      console.error('[AetherisSocket] Failed to parse incoming message:', err, event.data);
      return;
    }

    const { type, payload } = data;
    console.log(`[AetherisSocket] Received ← ${type}`, payload);

    switch (type) {
      case 'chat_response':
        this.onChatResponse(payload);
        break;

      case 'artifact_update':
        this.onArtifactUpdate(payload);
        break;

      case 'typing_indicator':
        this.onTypingIndicator(payload?.isTyping ?? false);
        break;

      case 'session_update':
        this.onSessionUpdate(payload);
        break;

      default:
        console.warn(`[AetherisSocket] Unknown message type: "${type}"`, payload);
    }
  }

  // ---------------------------------------------------------------------------
  // Public API Methods
  // ---------------------------------------------------------------------------

  /**
   * Send the completed onboarding data to the backend.
   * @param {object} data - The full onboarding form payload.
   */
  sendOnboardingData(data) {
    console.log('[AetherisSocket] Sending onboarding data…');
    this._send('onboarding_complete', data);
  }

  /**
   * Send a user chat message to the AI strategy engine.
   * @param {string} message - The user's message text.
   */
  sendChatMessage(message) {
    console.log('[AetherisSocket] Sending chat message…');
    this._send('chat_message', { message });
  }

  /**
   * Request the current list of strategy artifacts from the server.
   */
  requestArtifacts() {
    console.log('[AetherisSocket] Requesting artifacts…');
    this._send('get_artifacts', {});
  }

  /**
   * Submit user feedback for a specific AI message.
   * @param {string} messageId - The ID of the message being rated.
   * @param {number} rating    - Numeric rating (e.g. 1–5 or thumbs 0/1).
   */
  sendFeedback(messageId, rating) {
    console.log(`[AetherisSocket] Sending feedback for message ${messageId}…`);
    this._send('feedback', { messageId, rating });
  }
}

// =============================================================================
// Singleton Export
// =============================================================================

/**
 * Global singleton instance — import via `window.aetherisSocket` from app.js.
 * @type {AetherisSocket}
 */
const aetherisSocket = new AetherisSocket();
window.aetherisSocket = aetherisSocket;
