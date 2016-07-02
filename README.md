# Leankit Notifier

## Purpose

We use at work [Leankit](https://leankit.com/), and it has some small missing features (like notifications when a task is overdue, or some rules to enforce certain practices), so I decided to toy with their REST API in order to build a small script that can be run daily or connected to Slack to notify of cards (tasks) in the non-correct state.

Definition of correct state:
- Card is assigned to at least one person
- Card has a cost estimation (size)
- Card is not too big (size bigger than config provided field)
- Card has a date estimation (due date, although providing a starting date helps and allows additional checks)
- Card is not overdue


## Requisites

- Python 3
- An existing Leankit account

## Installation

- Copy `config.py.sample` to `config.py` and fill fields accordingly. Remember that authentication is a base64 of `username:password`

## Usage

- Just run `python3 leankit_notifier.py`

## TODO

- Take into account subcards? (we're not sure we want to have them with estimations and dates only inside)
- If subcards checked, there must be at least one subcard at "doing" lane
- Instead of current crappy prints, make it connect to a certain Slack channel and write there the report
