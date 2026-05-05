# Unity Shader Graph & VFX Graph — Fundamentals Reference

> Researched: 2026-02-23 | For: potuay-oracle VFX artist development

---

## Part 1: Shader Graph

### What is it?
Visual node-based shader authoring tool. No HLSL needed. Real-time preview.

### Key Concepts
- **Master Stack** — endpoint with Vertex & Fragment contexts (Base Color, Normal, Emission, Alpha, Metallic, Smoothness)
- **Nodes** — building blocks (math, texture, UV, procedural)
- **Properties** — exposed to Inspector (Color, Float, Texture2D, Vector, Boolean, Gradient)
- **Sub-graphs** — reusable shader functions
- **Custom Function Node** — inject raw HLSL when nodes aren't enough

### Shader Types
- **Lit** — PBR, responds to lights/shadows. For: game objects, characters, environments
- **Unlit** — no lighting. For: UI, hologram, stylized art, particles
- **Sprite Lit/Unlit** — 2D games
- **Decal** — project onto surfaces
- **Fullscreen** — post-processing

### Popular Effects

**Fresnel / Rim Lighting**
- `Fresnel Effect` node → Power 2-5 → Multiply by color → Emission
- Edges facing away from camera glow brighter

**Hologram**
- Unlit + Transparent surface
- Fresnel + Scanline (UV.y × Time through Sine)
- Low alpha + high Emission

**Dissolve**
- Noise texture → Step node vs threshold property → Alpha + Alpha Clipping
- Edge glow: Smoothstep near dissolve edge → Emission (fire color)

**Distortion / Water**
- Normal Map + Time offset UV → Scene Color sample
- Voronoi noise for caustics
- Depth-based transparency (Scene Depth vs Fragment Depth)

### Essential Nodes (Top 10)
1. Sample Texture 2D
2. UV / Tiling And Offset
3. Time
4. Multiply / Add
5. Lerp
6. Fresnel Effect
7. Simple Noise / Gradient Noise / Voronoi
8. Step / Smoothstep
9. Split / Combine
10. Remap

### Node Categories
| Category | Key Nodes |
|----------|-----------|
| Input > Basic | Float, Color, Vector2/3/4, Boolean, Time |
| Input > Texture | Sample Texture 2D, Sampler State |
| Input > Mesh | UV, Position, Normal Vector, Vertex Color, View Direction |
| Input > Scene | Scene Color, Scene Depth, Camera |
| Math > Basic | Add, Subtract, Multiply, Divide, Power |
| Math > Range | Clamp, Saturate, Remap, Fraction, Step, Smoothstep |
| UV | Tiling And Offset, Rotate, Twirl, Polar Coordinates |
| Procedural > Noise | Simple Noise, Gradient Noise, Voronoi |
| Procedural > Shape | Ellipse, Rectangle, Polygon |
| Artistic > Normal | Normal Strength, Normal Blend, Normal From Height |

### Performance Tips
- Remove unused nodes
- Multiply scalars before vectors (`float * float * float4`)
- Bake values into textures when possible
- Minimize texture samples; reuse via Split/Combine
- Use Vertex stage for cheaper per-vertex calculations
- Use `half` instead of `float` when possible
- Use Vector2 instead of Vector3 when possible
- Use built-in functions (`normalize`, `dot`)
- Profile with Frame Debugger

---

## Part 2: VFX Graph

### What is it?
GPU-based (Compute Shader) node-based particle system. Handles millions of particles.

### 4 Contexts

| Context | When Called | Purpose | Key Blocks |
|---------|-----------|---------|------------|
| **Spawn** | Every frame | How many particles to create | Constant Rate, Single Burst, Periodic Burst |
| **Initialize** | At particle birth | Set initial state | Set Position (Shape), Set Velocity, Set Lifetime, Set Size, Set Color |
| **Update** | Every frame per particle | Simulation | Turbulence, Force, Gravity, Linear Drag, Collision, Kill |
| **Output** | Every frame | Rendering | Quad, Mesh, Strip, Lit/Unlit, Blend modes |

### Common Effects

**Sparks** — Burst spawn → Random velocity up + spread → Gravity + Drag → Small quads + Additive

**Fire** — Constant high rate → Cone shape up → Turbulence + Size over life (shrink) + Color (orange→red→black) → Flipbook

**Smoke** — Slower, larger than fire → Gray→transparent → More turbulence

**Magic Aura** — Constant spawn → Sphere/circle shape → Orbit + Color over life → Additive + Trail

**Explosions** — Burst → High radial velocity → Multiple layers (flash, debris, smoke, shockwave)

### VFX Graph vs Particle System

| | VFX Graph | Particle System |
|--|-----------|-----------------|
| Runs on | **GPU** | CPU |
| Particle count | **Millions** | Thousands |
| Editing | Node-based graph | Inspector modules |
| C# access | Limited (events, properties) | Full read/write per-particle |
| Physics | No (GPU can't access CPU physics) | Yes |
| Learning curve | Steeper | Gentler |
| Platform | Needs Compute Shader | Runs everywhere |
| Best for | Large-scale VFX, weather, magic | UI effects, small gameplay FX, physics |

**Can combine both** — VFX Graph for GPU-heavy visuals + Particle System for physics interaction.

### Performance Tips
- Set **Capacity** as low as possible (affects memory)
- Match spawn rate to visual need
- **Watch overdraw** — overlapping transparent particles are expensive
- Use Kill block for off-screen particles
- Use Quad over Octagon when quality difference is negligible
- Reduce spawn rates at distance (LOD)
- Minimize turbulence/noise operations
- Profile with VFX Debug Panel, Unity Profiler, Frame Debugger

---

## Part 3: Shader Graph + VFX Graph Integration

1. Create Shader Graph → enable **"Support VFX Graph"** in Graph Settings
2. Assign to Output context in VFX Graph
3. Enables custom dissolve, distortion, stylized looks on particles
4. HDRP supports Lit, Eye, Hair, Fabric shader models on particles
5. Note: "Support VFX Graph" increases compile time but no runtime cost

---

## Part 4: URP vs HDRP

| | URP | HDRP |
|--|-----|------|
| Target | Mobile, broad, performance | PC/Console, high-end |
| VFX Graph | Supported (Unity 2021+) | Full support |
| Shader Graph | Supported | More features (Coat, Anisotropy, SSS) |
| Lit Particles | Basic lighting | Full PBR + volumetric, ray-traced |
| Recommendation | Start here (simpler) | For AAA quality |

**Critical**: Shader Graphs are pipeline-specific — URP shaders won't work in HDRP and vice versa.

---

## Part 5: Learning Resources

### Official
- [Unity Learn: Get Started with Shader Graph](https://learn.unity.com/tutorial/get-started-with-shader-graph)
- [Unity Learn: VFX Graph Fundamentals](https://learn.unity.com/course/vfx-graph-fundamentals)
- [Unity Docs: Shader Graph](https://docs.unity3d.com/Manual/shader-graph.html)
- [Unity Docs: VFX Graph](https://docs.unity3d.com/6000.2/Documentation/Manual/VFXGraph.html)
- [Unity 6 VFX Graph E-Book (free)](https://unity.com/resources/creating-advanced-vfx-unity6)

### YouTube & Tutorials
- **Gabriel Aguiar Prod** — Best Unity VFX tutorials (fire, magic, stylized)
- **Daniel Ilett** — Every Shader Graph node explained, hologram tutorial
- **Brackeys** — Classic Shader Graph beginner series (GitHub repo available)
- **Ben Cloward** — Advanced technical art
- **Binary Lunar** — Advanced VFX techniques

### Courses
- [Udemy: VFX Graph Beginner to Intermediate](https://www.udemy.com/course/unity-visual-effect-graph-beginner-to-intermediate/)
- [Udemy: Shader Graph for Beginners](https://www.udemy.com/course/shader-graph/)

### Community
- [Real Time VFX (realtimevfx.com)](https://realtimevfx.com) — Largest RT VFX artist community
- ArtStation — Portfolio inspiration

### Reference
- [Daniel Ilett: Every Shader Graph Node](https://danielilett.com/2021-05-20-every-shader-graph-node/)
- [Daniel Ilett: Hologram in URP](https://danielilett.com/2020-07-12-tut5-9-urp-hologram/)
- [z4gon/fire-vfx-unity (GitHub)](https://github.com/z4gon/fire-vfx-unity)

---

## Learning Roadmap

```
Week 1-2: Shader Graph Basics
  → Lit/Unlit shader, Fresnel, simple color effects
  → Hologram + Dissolve shader

Week 3-4: VFX Graph Basics
  → 4 Contexts, sparks, simple fire
  → Magic aura effect

Week 5-6: Combine Both
  → Custom Shader Graph for VFX Graph particles
  → Spell effect with dissolve particles

Week 7+: Advanced
  → Flipbook animation, mesh particles
  → Signed Distance Fields, event systems
  → Portfolio VFX reel
```
