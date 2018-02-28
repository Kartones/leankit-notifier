# Leankit Notifier

## Purpose

At TheMotion we used [Leankit](https://leankit.com/) to manage our tasks and projects, and it has some small missing features (like notifications when a task is overdue, or some rules to enforce certain practices), so I decided to toy with their REST API in order to build a small script that can be run daily or connected to Slack to notify of cards (tasks) in the non-correct state.

Definition of correct state:
- Card is assigned to at least one person
- Card has a cost estimation (size)
- Card is not too big (size bigger than config provided field)
- Card has a date estimation (due date, although providing a starting date helps and allows additional checks)
- Card is not overdue

**Note**: No longer in development. This tool might stop working at any time and I won't update it as I no longer use Leankit.

## Requisites

- Python 3
- An existing Leankit account

## Installation

- Copy `config.py.sample` to `config.py` and fill fields accordingly. Remember that authentication is a base64 of `username:password`

## Usage

- Just run `python3 leankit_notifier.py`
