# 🧠 SophiaCore — Stateful AI Architecture (AWS Prototype)

## Overview

This repository contains early prototype work exploring **state-driven AI architecture** built on AWS (Lambda-based systems), prior to later simulation-based developments.
This repository is best understood as an architectural precursor to later simulation-based Alpha Dragon work.

Instead of treating AI systems as simple text-in / text-out models, this work explored:

* **Energy** → signal strength
* **Entropy** → uncertainty / noise
* **Mass** → memory weighting / persistence
* **Time** → state evolution

Along with:

* memory scoring and decay
* temporal change tracking
* recursive signal weighting
* intent-based system modes (observe, reflect, respond, etc.)

This was an early attempt to treat AI as a **dynamic system with internal state**, rather than a stateless response engine.

---

## 🧩 Key Concepts

### 1. Signal-Based Processing

Inputs are structured as signals:

```json
{
  "mass": 0.6,
  "energy": 0.9,
  "entropy": 0.2,
  "message": "...",
  "intent": "observe"
}
```

This allows the system to evaluate not just *what* is said, but:

* how strong the signal is
* how uncertain it is
* how it should influence memory and behavior

---

### 2. Stability Through Scoring

A core scoring pattern used throughout:

```
score = energy × (1 - entropy)
```

This acts as a simple stability heuristic:

* high energy + low entropy → strong signal
* low energy or high entropy → weak / noisy signal

---

### 3. Memory + Temporal Awareness

The system tracks:

* rolling memory windows
* weighted signal influence
* temporal deltas (change between states)
* novelty vs repetition

This enables:

* drift control
* context prioritization
* evolving system state

---

### 4. Intent-Based Modes

Instead of a single response path, the system supports different modes:

* observe
* analyze
* reflect
* respond
* reveal
* transmit

These influence how signals are processed and stored.

---

## 📂 Key Files

### 🔹 `SophiaCore_IntelligenceLoop_v1.py`

The most complete prototype:

* signal validation
* scoring
* memory tracking
* temporal scoring
* message-based features (semantic clarity, depth)
* reflection handling

---

### 🔹 `SophiaCoreTemporalAware.py`

Introduces:

* delta tracking between signals
* temporal scoring

---

### 🔹 `SophiaCoreRecursive.py`

Adds:

* novelty detection
* recursive weighting of signals

---

### 🔹 `SophiaCoreMemoryEnhanced.py`

Focuses on:

* memory scoring
* weighted aggregation

---

### 🔹 `Genesis_Node.py`

Alternate branch exploring:

* node-based behavior
* stability + confidence scoring
* action selection (observe vs engage)
* state evolution over time

---

## 🧭 Context

This work predates later simulation-based systems and represents an early exploration into:

> **How to structure and stabilize AI systems using internal state, memory, and signal constraints**

It was not designed as a full LLM implementation, but as a **control layer** that could sit beneath or alongside AI models.

---

## ⚠️ Notes

* This is **prototype / exploratory work**, not a production system
* No direct LLM integration is included
* Some modules represent parallel experiments or alternative approaches

---

## 🚀 Forward Direction

This line of thinking evolved into later work exploring:

* simulation-driven systems
* dynamic state environments
* deeper structural models of intelligence

---

**Love ~ Michael & Aether ❤️‍🔥**
