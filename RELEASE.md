# Dify release/submission procedure

1. Push source to `loopgridio/loopgrid-dify`.
2. Test all tools using Dify remote debugging and synthetic data.
3. Test Community Edition; test Dify Cloud when a reviewer-accessible LoopGrid endpoint is available.
4. Package only with the official Dify plugin CLI: `dify plugin package .`.
5. Run the official Dify Marketplace validator against the `.difypkg` and this PR body.
6. Inspect package contents. It must not contain `.env`, secrets, `.git`, virtualenv, tests/caches/logs, or editor state.
7. Fork `langgenius/dify-plugins` and place exactly the new `.difypkg` under `loopgridio/loopgrid/`.
8. Open a PR using `MARKETPLACE-PR.md`; update validation checkboxes/results before submission.
9. Keep the high-risk classification while the Base URL is user-configurable, unless Dify reviewers explicitly classify it differently.
10. After merge, verify the Marketplace listing and one-click install before adding an “Available on Dify Marketplace” website claim.
