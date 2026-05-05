---
title: "Unity VFX Graph: Model Edges Bursts"
source: YouTube - Eric Wang_VFX Artist (https://www.youtube.com/watch?v=xxLg8Xw7S-c)
date: 2026-02-27
tags: [unity, vfx-graph, mesh-particles, burst, edges, urp]
unity_version: 2023.1.0b12 (video), 6000.0.64f1 (our project)
project: "D:\\vfx test"
---

# Model Edges Bursts — VFX Graph Technique

## Overview
Particles burst outward from the **edges** (sharp angles) of a 3D mesh model. Creates a dramatic "explosion along wireframe" look. By Eric Wang (VFX Artist).

## Core Technique

### 1. Spawn Context
- **Single Burst** mode — emits a large batch of particles at once
- Count: 5,000-50,000 depending on mesh complexity
- Can be triggered periodically or via event

### 2. Initialize Particle
- **Set Position from Mesh** — positions particles on the mesh surface
  - Source: Mesh (exposed property)
  - Placement mode: Edge / Surface
  - For "edges" effect: use edge placement or detect sharp normals
- **Set Velocity from Direction & Speed**
  - Direction: mesh surface normal (particles fly outward)
  - Speed: randomized for organic spread
- **Set Lifetime**: randomized (1-5 seconds)
- **Set Size**: small (0.01-0.1)
- **Set Color**: bright emission color

### 3. Update Particle
- **Turbulence** (Perlin noise) — organic movement
- **Age Particles** — standard aging
- Optional: Gravity, Drag for physics feel

### 4. Output Particle Quad
- **Blend Mode**: Additive (glowing look)
- **Color over Life**: bright → fade to transparent
- **Size over Life**: curve from 1 → 0 (shrink and disappear)
- Optional: Orient to velocity for streaks

## Key Properties (Blackboard)
| Name | Type | Default | Description |
|------|------|---------|-------------|
| TargetMesh | Mesh | - | The 3D model to burst from |
| ParticleCount | int | 5000 | Particles per burst |
| Lifetime | float | 3.0 | Max particle life |
| ParticleSize | float | 0.05 | Base size |
| VelocityScale | float | 2.0 | Outward speed |
| NormalForce | float | 1.5 | Normal direction strength |
| TurbulenceIntensity | float | 0.5 | Noise amount |
| BaseColor | Color | cyan | Main particle color |
| EdgeColor | Color | orange | Edge highlight color |

## Important Notes
- **Mesh Read/Write must be enabled** in import settings for VFX Graph to sample mesh data
- URP works but some advanced features (lit particles) need HDRP
- For best "edge" detection: use meshes with hard edges (not smoothed normals)
- Performance: GPU-based, can handle 50k+ particles easily on modern hardware

## Implementation
Created at: `D:\vfx test\Assets\VFX\ModelEdgesBurst\`
- `ModelEdgesBurstController.cs` — Runtime controller script
- `Editor\ModelEdgesBurstSetup.cs` — Editor window with step-by-step guide

## Related
- [Shader Graph & VFX Graph fundamentals](shader-graph-vfx-graph-fundamentals.md)
- Eric Wang Patreon: https://www.patreon.com/wangray
- Asset Store: https://assetstore.unity.com/packages/vfx/particles/vfx-graph-model-edges-bursts-290177
