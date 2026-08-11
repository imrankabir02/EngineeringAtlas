# Technology Selection

Popularity is not a reason. It is evidence about hiring markets and community
size, both of which matter, and neither of which tells you whether a technology
fits your problem.

Every technology mentioned in this repository must pass the rubric below. Any
technology that cannot answer **"when NOT to use it"** with something specific is
being sold rather than explained, and does not belong here.

---

## The rubric

Eight questions. All eight, or the technology is not documented.

### 1. What problem does it solve?

State it as a problem someone had before the technology existed. If the answer
requires the technology's own vocabulary, you have not answered it.

- Bad: "Kubernetes solves container orchestration."
- Good: "You have more containers than machines, containers die, machines die,
  and you need something to keep the declared set of workloads running and
  reachable without a human placing them."

### 2. When should you use it?

Concrete conditions, with rough thresholds where thresholds exist. "When you have
scaling needs" is not a condition; "when you are running more than a handful of
services across more than a handful of machines and are already paying for a
platform team" is.

### 3. When should you NOT use it?

**The most important question, and the one marketing never answers.**

Every technology has a region where it is a net loss. Name it. If you cannot,
you do not understand the technology yet — you understand its pitch.

### 4. What are the alternatives?

Including the two that are always on the list and always underrated:

- **Do nothing.** The current system may be adequate.
- **The boring option.** A relational database, a single process, a cron job, a
  file. These solve a remarkable share of problems, indefinitely.

### 5. What are the trade-offs?

What you *gave up*, stated as losses rather than as "considerations." Every
adoption is an exchange. If you cannot name what you lost, you have not looked.

### 6. What complexity does it add?

Operational complexity is the cost that gets omitted from every evaluation and
paid by every team. Count:

- Another thing to deploy, upgrade, monitor, back up, and secure
- Another failure mode, and its interaction with existing failure modes
- Another thing every new hire must learn
- Another thing to be woken up for

### 7. What is the ecosystem like?

Maturity, client library quality, documentation quality, release cadence,
governance (single vendor? foundation? one maintainer?), licence and its history
of changing, and how many people you could hire who already know it.

### 8. What does production look like?

The gap between the tutorial and production is where most cost lives. Backups and
*restores* (they are not the same thing), upgrades, capacity limits, observability
hooks, security defaults, multi-tenancy, and what it does when it is overloaded
rather than when it is healthy.

---

## Worked example: Redis

Written out fully, as the standard every technology entry in this repository
should meet.

### Problem

Reading from a relational database over a network, executing a query plan against
disk-backed pages, costs milliseconds. Some data is read thousands of times more
often than it changes. Redis provides microsecond-scale access to that data by
keeping it in memory, in a process built for one job.

Secondarily, it provides a *shared* place for ephemeral state that many
application processes must agree on — sessions, rate-limit counters, locks, job
queues — which a per-process in-memory cache cannot do.

### Use when

- A cacheable read is hot enough that the cache will actually be hit. Below a
  meaningful hit ratio you have added a network hop and a failure mode for
  nothing.
- Multiple processes must share ephemeral state and losing it is survivable.
- You need a data structure server: sorted sets for leaderboards and sliding
  windows, sets for membership, streams for a simple log, HyperLogLog for
  approximate cardinality. This is Redis's genuinely distinctive capability, and
  the reason it wins over Memcached more often than raw speed does.
- You need a simple job queue and can accept its delivery guarantees.

### Avoid when

- **It would be your only copy of important data.** Redis persistence (RDB
  snapshots, AOF) exists and works, but the durability model is weaker than a
  database designed for durability, and the failure mode is silent data loss on
  an unclean shutdown between fsyncs. If losing it means losing money, it belongs
  in a database.
- **A single process needs the cache.** An in-process cache is faster, simpler,
  and has no network partition. Reach for Redis when you need *sharing*.
- **The dataset does not fit in memory,** and you were planning to rely on
  eviction to hide that. You will get a low hit ratio, unpredictable latency, and
  a large bill.
- **The underlying query is slow because it is badly written or missing an
  index.** Caching a 4-second query gives you a 4-second query that fires on
  every cache miss, at the worst possible moment. Fix the query first; this is
  the single most common misuse.
- **You need queries.** Redis is a key-value store with data structures. If you
  find yourself maintaining secondary indexes by hand in application code, you
  have reimplemented a database badly.
- **You need strong consistency across a cluster.** Redis Cluster is
  asynchronously replicated; a failover can lose acknowledged writes. Redlock is
  contested as a correctness primitive — read both Kleppmann's critique and
  Sanfilippo's reply before you build on distributed locks.

### Alternatives

| Alternative | Prefer it when |
|---|---|
| In-process cache (a map, an LRU, `functools.lru_cache`) | One process; no sharing needed. Always try this first. |
| Memcached | Pure cache, simple strings, multi-threaded scaling on big boxes, and you want fewer features to misuse. |
| The database itself | Materialised views, better indexes, or the DB's own buffer cache may be enough. Measure before adding a tier. |
| CDN / HTTP caching | The data is public and addressable by URL. Then the cache is free and geographically distributed. |
| Postgres `UNLOGGED` tables or a JSONB column | You want one fewer system to operate and the latency budget allows it. |
| Kafka / a real broker | You are using Redis lists as a queue and now need durability, replay, or consumer groups. |
| Valkey | You want Redis's semantics under a BSD licence with foundation governance, after the 2024 licence change. |

### Trade-offs

- You gained latency; you gave up **having one source of truth**. Every cache is
  a second copy that can be wrong, and invalidation bugs are among the hardest to
  reproduce, because they depend on timing and on traffic you did not generate.
- You gained a fast shared store; you gave up **failure independence**. Your
  application now has a new dependency whose unavailability you must handle, and
  a cold cache after a restart can mean a thundering herd that takes down the
  origin you were protecting.
- Single-threaded command execution buys you atomicity and simple reasoning; it
  costs you a **hard ceiling on per-instance throughput** and means one `KEYS *`
  or a large `Lua` script blocks every other client.
- Memory is the constraint, and memory is expensive. Fragmentation, per-key
  overhead, and copy-on-write during snapshotting mean actual usage exceeds your
  arithmetic — plan headroom.

### Complexity added

One more service to deploy, monitor, secure, upgrade, and page someone about.
New questions you must now answer: max-memory policy, persistence configuration,
whether you need replication and what failover does to in-flight writes,
connection pool sizing, key naming and TTL discipline, and how the application
behaves when Redis is down (degrade to origin? fail? serve stale?). Answer that
last one deliberately, on paper, before you ship.

### Production considerations

Set `maxmemory` and `maxmemory-policy` explicitly — the default behaviour on
memory exhaustion is not what you want. Monitor hit ratio, evicted keys, memory
fragmentation ratio, blocked clients, and replication lag; hit ratio alone is not
enough. Never expose it to a network you do not control; historically Redis
assumed a trusted network, and internet-reachable instances are compromised
routinely. Test a restore, not just a backup. Know your `SCAN`-vs-`KEYS` policy
before an incident, not during one.

---

## Where this rubric lives in the content

- Each technology-oriented topic answers the eight questions in `practical.md`
  under a **"Selection"** heading.
- `topic.yml` records `version_sensitivity`, because a technology that changes
  quickly needs its concrete guidance quarantined from its conceptual guidance.
  See [version-awareness.md](version-awareness.md).
- Paths must never recommend a technology without a link to the topic that
  contains its rubric. A path that says "add Kafka" without linking to the
  trade-offs is doing the thing this document exists to prevent.
