# First PC setup

This repository currently contains **planning files only**. There is no runnable Unreal project yet.

1. Install a supported Unreal Engine 5 release, Visual Studio with C++ game development tools, and Git/GitHub Desktop.
2. Clone the `main` branch of `brylancreatesart-cell/DeadShift` to a local folder.
3. In Unreal Engine, create a **Games > Third Person > C++** project named `DeadShift`. Place it in this repository directory, avoiding an extra nested `DeadShift/DeadShift` folder.
4. If Unreal refuses to create inside a nonempty directory, create it in a temporary location and copy its generated project files into the cloned repository root.
5. Open the generated `.uproject`, allow project files/modules to build, and verify the template works before adding new networking code.
6. Commit the generated Unreal project files (not cache/build output), then push to GitHub.
7. Set up a two-client PIE test and document the result.

**Warning:** Any local clone made before the November 2026 reset still points at the archived history. Make a fresh clone or intentionally reconcile branches; do not blindly pull over uncommitted work.

Keep story drafts in Codex until explicitly approved for integration.
