# Python backend engineer

**Level 1 → Level 4** · roughly 18 months–3 years part-time · assumes you can write small Python
programs

Machine-readable steps: [`python-backend.yml`](python-backend.yml)
Prerequisite path: [absolute-beginner](../absolute-beginner.md)

---

## Who this is for

Someone who can write and debug small Python programs and wants to build and operate **production**
Python services — not scripts, not notebooks, and not tutorial projects.

The path ends here:

> You are accountable for a Python service in production: you can size it, cost it, debug it from
> its telemetry, and state what you sacrificed in its design.

---

## Read this first: what a stack path actually is

This is the reference stack path, and the most important thing about it is structural.

**Count the steps.** There are 46. Of those, **fewer than ten are Python-specific in any real
sense.** The rest are shared topics — `http`, `sql`, `caching`, `concurrency-and-parallelism`,
`observability` — that any backend engineer needs regardless of language.

What makes this a *Python* path is the **emphasis** on each step: what specifically matters about
that topic in Python, which idioms to use, which library is the current default, and which of
Python's peculiarities will bite you. Those paragraphs are the path's actual content. The topics
themselves live once in [`topics/`](../../topics/) and are shared with every other path — see
[architecture.md §5](../../docs/architecture.md#5-languages-and-stacks-are-paths-not-topics).

This has a consequence worth knowing at the start, because it is the honest lesson:

> Roughly 80% of what you learn here transfers to Go, Java, Node, or PHP. The remaining 20% is
> Python's answer to questions every language has to answer.

That is why "which language should I learn first?" matters much less than people think, and why the
correct response to a hard topic is never to switch languages.

---

## Phase 1 — Python properly

**8 steps · ~250 hours · 6–8 months**

`error-handling` → `debugging-fundamentals` → `type-systems` →
`object-oriented-programming` → `functional-programming` → `testing-fundamentals` →
`package-management` → `clean-code`

You can already write Python. This phase is about writing it the way the language wants, and about
the general engineering practices, learned through Python.

The steps where Python is genuinely distinctive:

**`type-systems`.** Python's type hints are optional and gradual, which makes it an unusually good
place to learn what static checking is *for*. Add hints and mypy or pyright to an existing project
of yours and count the real bugs found. That number will change your opinion more than any argument
about static versus dynamic typing.

**`object-oriented-programming`.** `dataclasses` for data, `Protocol` for structural interfaces,
composition over inheritance. Deep hierarchies are rarer in Python than in Java, and the reason is
instructive: duck typing removes most of the motivation for them. The real interface system in
Python is the **dunder methods** — `__len__`, `__iter__`, `__enter__` — which is a genuinely different
design from nominal interfaces, and worth understanding as a design choice rather than a quirk.

**`functional-programming`.** Comprehensions, generators, and `itertools`. Generators are the
idiomatic way to process data larger than memory, and their laziness surprises everyone exactly
once — usually by a generator being consumed before you expected.

**`testing-fundamentals`.** pytest: fixtures, `parametrize`, `monkeypatch`. The judgment call that
matters is **what not to mock**. Mocking things you do not own produces tests that pass while
production breaks, because you have encoded your belief about the dependency rather than its
behaviour.

**`package-management`.** Virtual environments, `pyproject.toml`, and a lockfile. Use uv or Poetry
over bare pip for anything real. Python's packaging story is fragmented, and it is worth
understanding *why* — the history explains the tooling, and it stops the confusion feeling like your
fault.

**Milestone.** You can build a tested, typed, installable Python package with a CLI, and you can
explain what your type checker caught that your tests would not have.

---

## Phase 2 — the web and data layer

**11 steps · ~330 hours · 8–11 months**

`linux-fundamentals` → `networking-fundamentals` → `http` →
`tls-and-cryptography-basics` → `databases-introduction` → `sql` →
`relational-modeling` → `rest-apis` → `authentication-and-authorization` →
`backend-development` → `git-workflows`

**`http` before any framework.** Read the relevant RFC sections rather than a Django or FastAPI
tutorial. Every Python web framework is a thin layer over HTTP semantics, and the semantics are what
transfer. A framework learned without them leaves you unable to debug anything that happens at the
protocol level, which is where a surprising share of production problems live.

**`sql` before any ORM.** Write queries by hand first. Then, when you use SQLAlchemy or the Django
ORM, you can read what it generated — and you will need to, because the characteristic
Python-web performance bug is the **N+1 query**, where the ORM helpfully issues one query per row of
a loop. You cannot see it without reading the emitted SQL.

**`relational-modeling`.** Put constraints in the database, not only in your models. A `NOT NULL`
the database enforces survives a buggy migration script and a colleague's `manage.py shell`
session; a validator in Python does not.

**`rest-apis` and `backend-development`** are where the framework choice arrives:

| Framework | Choose when | Cost |
|---|---|---|
| **FastAPI** | API-first service; you want type hints to become runtime validation via Pydantic | You assemble more yourself: no admin, no ORM, no auth out of the box |
| **Django** + DRF | Larger application; you want the admin, the ORM, migrations, and conventions | More framework to learn, and its conventions are opinionated |
| **Flask** | Something small, or you want to see the pieces | You will end up assembling a framework, less well |

FastAPI is the current default for new API services, and the pairing with type hints is genuinely
good — the same annotations serve documentation, validation, and the type checker. Django remains the
better answer for anything with substantial admin and content needs.

Whichever you choose, the transferable content is resource modelling, status codes, idempotency, and
error design — not the framework's decorators.

**`authentication-and-authorization`.** Use the framework's implementation. Password hashing with
argon2 or bcrypt via passlib, never your own. Know why JWTs are awkward to revoke *before* choosing
them over server-side sessions; the choice is usually made by default and regretted later.

**Milestone.** You have deployed a Python service with a real database, migrations, authentication,
and a test suite you rely on when refactoring. You can read the SQL your ORM emits.

---

## Phase 3 — making it survive reality

**12 steps · ~450 hours · 10–14 months**

`data-structures` → `complexity-analysis` → `operating-systems-fundamentals` →
`concurrency-and-parallelism` → `async-programming` → `transactions-and-isolation` →
`indexing-and-query-optimization` → `caching` → `background-jobs-and-queues` →
`test-strategy` → `software-design-principles` → `software-architecture`

This phase contains the Python-specific material that most affects architecture.

### Concurrency, and the GIL

The single most consequential Python-specific fact, and the most commonly misunderstood.

The global interpreter lock means **only one thread executes Python bytecode at a time**. So:

- **Threads do not give you CPU parallelism.** Four threads on four cores computing something will
  not be four times faster.
- **Threads do give you I/O concurrency.** While a thread waits on a socket or a disk read, the lock
  is released and another thread runs. For an I/O-bound service — which most web services are —
  threads work fine.
- **CPU-bound work needs processes**, via `multiprocessing` or a worker pool, which means paying for
  inter-process communication and separate memory.

`operating-systems-fundamentals` is a hard prerequisite here for exactly this reason: without
knowing what a thread and a process actually are, the GIL is folklore rather than a constraint you
can reason about.

Free-threaded Python builds — where the GIL can be disabled — are progressing. *Verified as of
2026-08:* they exist, they are not the default, and library support is incomplete. Watch them; do
not architect around them yet.

### Async

asyncio, and one rule that matters more than all the others:

> **One blocking call in an async handler stalls the entire event loop.**

Not that request — the whole loop, and therefore every concurrent request in that process. A
synchronous database driver, a `requests` call, or a CPU-heavy loop inside an `async def` will do
this. Know which of your libraries are async-native and which need to be pushed to a thread pool.

Also: **do not make everything async by default.** It is a real complexity cost — two ecosystems of
libraries, harder debugging, and stack traces that tell you less. Async pays off when you have many
concurrent I/O-bound connections. For a service handling moderate traffic, threaded synchronous code
is simpler and often fast enough.

### Data under pressure

`transactions-and-isolation` — know your framework's default transaction boundary. Django wraps a
request in a transaction only if you enable `ATOMIC_REQUESTS`; SQLAlchemy's session behaviour depends
on how you configured it. Then check your *database's* default isolation level rather than assuming
it.

`indexing-and-query-optimization` — read the execution plan, not the ORM. Learn your ORM's
eager-loading mechanism (`select_related` / `prefetch_related`, or `joinedload`) early, because the
N+1 query is the bug you will fix most often.

`caching` — `functools.lru_cache` for in-process, Redis for shared. And cause a stampede yourself
before trusting anything you read about caching; the
[project](../../projects/in-memory-cache/README.md) makes it cheap.

`background-jobs-and-queues` — Celery is the incumbent and is operationally heavy. RQ and Dramatiq
are simpler. A database table plus a worker loop is a legitimate answer at low volume, and choosing
it deliberately is a sign of judgment rather than laziness. Whichever you use, **idempotent handlers
matter more than the library**, because a job will be delivered twice eventually.

**Milestone.** Your service handles concurrent load, has a measured performance profile, and you can
explain the GIL's consequences for your architecture rather than repeating that it exists.

---

## Phase 4 — operating it

**15 steps · ~600 hours · 12–20 months, mostly on the job**

`processes-and-scheduling` → `containers-and-docker` → `ci-cd` →
`linux-administration` → `cloud-fundamentals` → `infrastructure-as-code` →
`observability` → `security-fundamentals` → `application-security` →
`distributed-systems-fundamentals` → `message-queues-and-streaming` →
`partitioning-and-sharding` → `system-design-fundamentals` →
`performance-engineering` → `kubernetes` → `large-scale-system-design`

Python-specific notes on the operational steps:

**`containers-and-docker`.** Multi-stage builds, a non-root user, pinned dependencies. Know why the
naive Python image is over a gigabyte and how to get it to about 100 MB — the answer involves build
dependencies, wheel caching, and slim base images, and working it out teaches you more about images
than any tutorial.

**`ci-cd`.** Lint, type-check, test, build, deploy, with a rollback you have actually tested. **Run
the type checker in CI** or your annotations will quietly stop being true within a month.

**`observability`.** Structured logging over `print`, OpenTelemetry for traces, and metrics with
bounded cardinality. In an async service, a distributed trace is worth more than any amount of
logging, because the interleaving is the thing you cannot reconstruct from logs.

**`application-security`.** The ORM protects you from SQL injection **only while you use it
correctly** — a raw query built with an f-string undoes it entirely. Also: never `pickle` untrusted
data (it executes arbitrary code by design), and treat dependency risk as real, since a Python
project has a large transitive dependency tree.

**`performance-engineering`.** py-spy for profiling production without restarting it — this is a
genuine Python advantage and worth knowing exists. cProfile for development, memray for memory.
Measure before optimising; Python's slow parts are rarely where you guess, and the answer is
frequently "the database" rather than the interpreter.

**`kubernetes`.** Learn it if you operate it. And be able to say when a single machine with systemd
and a reverse proxy would have been the better answer — for a great many Python services, it is.
Being able to decline complexity credibly is a Level 4 skill.

**Milestone.** You are accountable for a Python service in production: you can size it, cost it,
debug it from its telemetry, and state what you sacrificed in its design. **Level 4.**

---

## Honest effort estimate

| Phase | Steps | Focused hours | Calendar at ~10 h/week |
|---|---|---|---|
| 1 — Python properly | 8 | ~250 | 6 months |
| 2 — web and data | 11 | ~330 | 8 months |
| 3 — surviving reality | 12 | ~450 | 11 months |
| 4 — operating it | 16 | ~600 | 14 months |
| **Total** | **47** | **~1,630** | **~3.2 years** |

At 20 hours a week, roughly 19 months. Phase 4 overlaps heavily with employment — you cannot learn
incident response without incidents — so getting a job after phase 2 and continuing on it is the
normal route and changes the calendar substantially.

---

## Where people stall

**Starting with a framework.** Django or FastAPI before `http` and `sql` works right up until
something breaks at the protocol or query level, and then there is nothing to fall back on. This is
the single most common failure mode for Python backend engineers and it is entirely avoidable.

**Fighting the packaging ecosystem.** It is genuinely fragmented and it is not your fault. Pick uv
or Poetry, use it consistently, and move on. Do not spend a month on tooling archaeology.

**Believing async is always better.** It is a complexity cost with a specific payoff. Threaded
synchronous Python handles a great deal of real traffic, and choosing it deliberately is correct more
often than the discourse suggests.

**Repeating "the GIL makes Python slow".** The GIL affects CPU-bound *parallelism* in threads.
Most web services are I/O-bound, where it is close to irrelevant. Being precise about this is a
credibility marker in interviews and design discussions.

**Never reading the emitted SQL.** The ORM is a convenience, not an abstraction you can afford to
trust blindly. Turn on query logging in development and look at what your endpoints actually do —
most people are shocked the first time.

---

## Related paths

| Path | Relationship |
|---|---|
| [Software engineering core](../software-engineering-core.md) | The language-neutral spine. ~80% of this path's steps come from it |
| [Programming foundations](../programming-foundations.md) | Phase 1 of this path, without the Python emphasis |
| [Computer science foundations](../computer-science-foundations.md) | Deeper on the theory this path touches lightly |

**On learning a second language.** After phase 3, a second language chosen for contrast — Go for
explicit concurrency and errors, Rust for ownership, or a Lisp for a genuinely different model — is
one of the highest-value things you can do. It is where you find out which of your knowledge was
Python and which was engineering, and the answer is usually reassuring.
