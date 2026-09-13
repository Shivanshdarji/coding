import { useState, useEffect, useRef, useCallback } from 'react';

export function useSpeechRecognition({
    onResult,
    onEnd,
    onError,
    enabled = true,
    isBlocked = false
}) {
    const [isListening, setIsListening] = useState(false);
    const [error, setError] = useState(null);
    const recognitionRef = useRef(null);
    const silenceTimerRef = useRef(null);
    const isBlockedRef = useRef(isBlocked);

    const enabledRef = useRef(enabled);

    // Update ref when prop changes so internal callbacks see current value
    useEffect(() => {
        isBlockedRef.current = isBlocked;
        enabledRef.current = enabled;
        if (isBlocked || !enabled) {
            stop();
        } else if (enabled && !isListening) {
            start();
        }
    }, [isBlocked, enabled]);

    const start = useCallback(() => {
        if (isBlockedRef.current || !enabled) return;

        // Prevent multiple instances
        if (recognitionRef.current) {
            try {
                recognitionRef.current.stop();
            } catch (e) { }
        }

        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) {
            setError("Speech Recognition not supported");
            return;
        }

        const recognition = new SR();
        recognition.lang = "en-US";
        recognition.interimResults = true;
        recognition.continuous = true;
        recognition.maxAlternatives = 1;

        let finalTranscript = '';

        recognition.onstart = () => {
            setIsListening(true);
            setError(null);
            console.log("🎤 Voice: Listening started");
        };

        recognition.onresult = (event) => {
            let interim = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + ' ';
                } else {
                    interim += event.results[i][0].transcript;
                }
            }

            // Reset silence timer
            if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);

            // Silence Detection (2 seconds)
            silenceTimerRef.current = setTimeout(() => {
                const fullText = (finalTranscript + interim).trim();
                if (fullText.length > 1) {
                    console.log("🎤 Voice: Final result:", fullText);
                    stop(); // Stop listening
                    onResult(fullText); // Send result
                    finalTranscript = '';
                }
            }, 2000);
        };

        recognition.onerror = (event) => {
            if (event.error === 'no-speech') {
                // Ignore no-speech, let it restart
                return;
            }
            if (event.error !== 'aborted') {
                console.warn("🎤 Voice Error:", event.error);
                setError(event.error);
                if (onError) onError(event.error);
            }
        };

        recognition.onend = () => {
            setIsListening(false);
            if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);

            // Auto-restart if enabled and not blocked
            if (enabledRef.current && !isBlockedRef.current) {
                setTimeout(() => {
                    start();
                }, 300);
            } else {
                if (onEnd) onEnd();
            }
        };

        try {
            recognition.start();
            recognitionRef.current = recognition;
        } catch (e) {
            console.error("🎤 Voice: Failed to start", e);
        }
    }, [enabled, onResult, onEnd, onError]);

    const stop = useCallback(() => {
        if (silenceTimerRef.current) clearTimeout(silenceTimerRef.current);
        if (recognitionRef.current) {
            try {
                recognitionRef.current.abort(); // Abort is faster than stop
            } catch (e) { }
            recognitionRef.current = null;
        }
        setIsListening(false);
    }, []);

    // Cleanup
    useEffect(() => {
        return () => {
            stop();
        };
    }, [stop]);

    return {
        isListening,
        error,
        start,
        stop
    };
}
