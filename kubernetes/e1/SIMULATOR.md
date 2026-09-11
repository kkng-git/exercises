# Datadog observability simulator

The `simulator-loadgen` deployment sends one request every two seconds to the API.
Requests are distributed across these scenarios:

- `healthy` (75%): checks PostgreSQL and returns HTTP 200.
- `slow` (15%): waits 0.8-1.8 seconds, checks PostgreSQL, and returns HTTP 200.
- `error` (10%): raises an intentional exception and returns HTTP 500.

Every request produces:

- custom DogStatsD metrics: `three_tier.simulator.requests`,
  `three_tier.simulator.request.duration`, and `three_tier.simulator.errors`;
- a Flask request trace with a child `simulator.work` span and PostgreSQL spans;
- a structured JSON completion log with `scenario`, `status_code`, `duration_ms`,
  `request_id`, `dd.trace_id`, and `dd.span_id` fields.

## Datadog views

Data can take a few minutes to appear after a fresh deployment.

- Metrics Explorer: graph `sum:three_tier.simulator.requests{env:lab} by {scenario}`.
- APM > Traces: query `service:three-tier-api env:lab`.
- Logs Explorer: query `service:three-tier-api env:lab`.
- Kubernetes Explorer: filter by `kube_namespace:three-tier-app`.

To force one scenario locally:

```sh
kubectl -n three-tier-app port-forward service/api-service 5000:5000
curl http://localhost:5000/simulate/healthy
curl http://localhost:5000/simulate/slow
curl http://localhost:5000/simulate/error
```

Pause or resume automatic traffic with:

```sh
kubectl -n three-tier-app scale deployment simulator-loadgen --replicas=0
kubectl -n three-tier-app scale deployment simulator-loadgen --replicas=1
```
