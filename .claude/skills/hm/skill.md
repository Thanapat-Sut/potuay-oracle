# /hm — Humanize Code

> Make code look like an intermediate programmer wrote it.

## Usage

```
/hm                     — humanize all files changed in this session
/hm path/to/file.cs     — humanize specific file
```

## Rules

Read the target file(s), then apply these transformations:

### Comments
- XML `<summary>` docs → short `//` one-liners or remove if obvious
- Keep comments only where logic isn't self-evident
- Write like notes-to-self: `// skip legendary color` not `// Excludes the Legendary target color during an active Legendary command so only the cluster tiles represent that color on the floor`
- Occasional typo in comments is fine (but not in code)

### Naming
- Prefer shorter common names: `count` over `colorCount`, `picks` over `candidates`, `held` over `heldTile`
- Use `i`, `j`, `c`, `t` for loop/temp vars
- Don't rename public API or serialized fields

### Structure
- Inline small helper methods (< 5 lines) that are called only once
- Collapse single-statement if/else into one line when readable
- Don't over-extract — 3 similar lines > premature abstraction
- Keep blank lines minimal but not zero

### Style
- Mix brace styles slightly (most on new line, occasional same-line for short blocks)
- Don't align assignments or declarations into columns
- Occasional `var` mixed with explicit types

### Do NOT change
- Logic, behavior, or output
- Public method signatures
- SerializeField or Inspector-visible members
- Enum values or class names
- Anything that would break compilation

## Tone Target

60-70% polished. Not sloppy, not perfect. Code that works well, reads fine, but clearly wasn't written by an AI or a senior architect.
