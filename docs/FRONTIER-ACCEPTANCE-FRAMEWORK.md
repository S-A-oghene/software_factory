# Software_Factory v0.1.0 Frontier Acceptance Framework

## 1. Purpose

This framework measures both the factory and the systems it generates. It prevents a passing coding loop from being mistaken for frontier engineering capability.

## 2. Ten KPI families

### 2.1 Specification Realization Index (SRI)

```text
SRI = weighted requirements demonstrably satisfied / weighted requirements specified
```

Recommended release gates:

- 100% of critical requirements implemented and tested;
- >=95% weighted requirement realization;
- no critical requirement left as merely claimed.

### 2.2 End-to-End Business Journey Success Rate (E2EJSR)

```text
E2EJSR = critical journeys completed correctly / critical journeys attempted
```

Recommended gates:

- 100% of critical journeys;
- >=95% of all defined non-critical journeys.

### 2.3 Architecture Maturity Index (AMI)

Evaluate whether the solution demonstrates appropriate:

- separation of concerns;
- bounded contexts/domains;
- explicit state transitions;
- idempotency;
- retry/dead-letter semantics;
- failure isolation;
- security boundaries;
- observability;
- portability/provider abstraction;
- scale-out paths;
- governance;
- testability.

### 2.4 Non-Functional Quality

Measure, where relevant:

- latency;
- throughput;
- concurrency;
- resource use;
- scalability;
- fault recovery;
- restart/replay;
- deployment/recovery operations;
- usability and accessibility.

### 2.5 Security Critical Defect Rate

Hard gate:

```text
0 unresolved critical security findings at release
```

Also test secret exposure, privilege boundaries, injection, unsafe tool use, cross-workspace access and supply-chain hygiene.

### 2.6 Portability / Provider Independence

Use actual migration exercises rather than merely looking for adapter classes.

```text
PIR = capabilities executable through provider adapters / total declared portable capabilities
```

Each portability claim must be backed by an executable or deterministic migration test.

### 2.7 Autonomous Engineering Ratio (AER)

```text
AER = 1 - human engineering interventions / total engineering interventions required
```

Separate approval-only interactions from human implementation/debugging so autonomy is not overstated.

### 2.8 Repair and Resilience

Measure:

```text
ARSR = recoverable failures autonomously repaired / recoverable failures
RFRR = regression-free repairs / successful repairs
```

Recommended v0.1 gates:

- >=80% autonomous repair success on recoverable seeded failures;
- >=90% regression-free successful repairs.

### 2.9 Evidence Coverage

```text
EC = material engineering claims backed by executable or auditable evidence / material engineering claims
```

Recommended gate: >=95%.

### 2.10 Frontier Benchmark Performance

Compare factory-generated solutions against a strong independent reference using identical challenge specifications and test suites.

Evaluate independently:

- functionality;
- architecture;
- performance;
- security;
- resilience;
- operability;
- portability;
- engineering effort;
- time;
- cost where measurable.

Do not reduce this to one opaque score.

## 3. Novelty and emergence

### Novel Generation Rate (NGR)

```text
NGR = novel tasks solved / novel tasks attempted
```

The challenge set must contain requirements not trivially represented by the template library.

### Architecture Emergence Index (AEI)

Ask whether the factory can create a materially different architecture when constraints require it. Examples include geographic partitioning, eventual consistency, offline operation, extreme auditability or regional failure.

## 4. AMPA-aligned future metrics

AMPA's own system-level metrics remain distinct from v0.1 factory metrics. Future physical-system evaluation includes:

- Mean Time Between Human Interventions;
- Automation Rate for Novel Tasks;
- Resource Independence Ratio;
- Mean Time To Recovery;
- Graceful Degradation;
- Material Adaptation;
- Learning Rate;
- Error Recurrence Rate;
- Simulation-to-Reality Gap.

v0.1 should prove it can architect and instrument systems capable of being measured against these later.

## 5. Hard release gates

| KPI | v0.1.0 release gate |
|---|---:|
| Critical requirement realization | 100% |
| Weighted requirement realization | >=95% |
| Critical E2E journeys | 100% pass |
| Other E2E journeys | >=95% pass |
| Unresolved critical security defects | 0 |
| Critical governance violations | 0 |
| Evidence coverage | >=95% |
| Autonomous repair success | >=80% of recoverable seeded failures |
| Regression-free autonomous repairs | >=90% |
| Human implementation intervention | <=10% of generated tasks on benchmark |
| Declared portable capabilities passing migration test | 100% |
| Reference functional parity | >=95% on defined benchmark |
| Reference critical-NFR regression | none |
| Independent review | required |

These numeric thresholds are **project acceptance proposals**, not claims about external industry standards.

## 6. Benchmark record

Every benchmark run must retain:

- specification hash;
- factory commit/version;
- model/provider identity if used;
- prompt/context bundle hash;
- generated artifact hash;
- validation outputs;
- security outputs;
- performance outputs;
- reviewer decisions;
- reference implementation/version;
- deviations and unresolved research assumptions.
