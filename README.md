# Nudge

Nudge is a lightweight, ambient fact reviewer for macOS. It's an experiment in gentle learning, designed to integrate into a study workflow, not interrupt it. It floats, it reminds, and then it disappears.

## The Philosophy

The digital tools we use for studying are often aggressive, demanding our full attention and turning the marathon of medical school into a series of frantic sprints. I wanted to build the opposite.

Nudge was born from a desire for a softer, more integrated way to learn—a tool that respects your focus by refusing to demand it. It does not track streaks or yell at you for being wrong. It simply introduces a single fact into your awareness, asks for a moment of engagement, and trusts the process. It is a study companion built for the quiet spaces in between.

## Features

*   **Aesthetic First:** The entire interface is built around a custom, soft color palette to create a digital workspace that feels personal and humane.
*   **Ambient & Unobtrusive:** A borderless, movable pop-up appears periodically, feeling like a gentle overlay rather than a harsh alert.
*   **Simple Interaction:** Two clear choices—"I remember!" or "I forgot!"—reveal the answer, followed by a graceful option to end the session.
*   **User-Controlled Content:** All questions are pulled from a simple `questions.csv` file, making the content transparent and incredibly easy to update.
*   **Stable & Lightweight:** Built with Python and `FreeSimpleGUI`, the final script runs as a simple background process without freezing or demanding system resources.

## How It Works

This app was built from scratch, starting with a simple idea and evolving through a dozen versions to solve the unique challenges of GUI development on macOS. The final version uses a non-blocking event loop to ensure it remains responsive and a simple `try...finally` structure to guarantee a graceful shutdown.

The core logic lives in `app.py`, while the study content is entirely managed by `questions.csv`.

## How to Use

1.  Ensure you have Python and `FreeSimpleGUI` installed.
2.  Customize the `questions.csv` file with your own one-liner facts.
3.  Run the script from your terminal: `python3 app.py`
4.  To end the session, press `Control + C` in the terminal or click the End Session button. A goodbye message will appear.

This project was a personal exploration in building the tools I wish existed: a testament to the idea that our digital environments should be as thoughtfully designed as our physical ones.
