#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &

# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieveing model mistral-nemo:12b..."
ollama pull mistral-nemo:12b
echo "🟢 Done!"

echo "🔴 Retrieveing model embeddinggemma:300m..."
ollama pull embeddinggemma:300m
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
