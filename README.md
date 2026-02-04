# Next Cycle Planning & Tracking

A local dashboard to track Redmine story readiness for the upcoming cycle. It visualizes the pipeline (No ET → Ready) and groups stories by PM.

## Prerequisites

1. **Python** must be installed.
2. **Git** must be installed.

## Installation

Open your terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
pip install git+https://github.com/avalenta-11/pm_next_cycle_tracker.git
```

## How to Run

Run the following command in your terminal:

```bash
start-tracker
```

## First-Time Configuration

When you run the tool for the first time, go to the Settings tab in the dashboard and fill in the following:

1. Redmine Base URL (no trailing slash).
2. Redmine API Key.
3. C+1 (Next Cycle) Version ID.

## How to Update

```bash
pip install --upgrade git+https://github.com/avalenta-11/pm_next_cycle_tracker.git
```

## How to Remove

```bash
pip uninstall pm_next_cycle_tracker
```