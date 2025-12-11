# Noise-Generator

## Table of contents

- [Features](#features)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
- [Usage](#usage)
  - [Library (Node.js) example](#library-nodejs-example)
  - [CLI example](#cli-example)
- [Configuration / Options](#configuration--options)
- [Examples](#examples)
- [Tests](#tests)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- Generate common noise types:
  - White, Pink, Brown (Brownian)
  - Perlin and Simplex noise (for procedural textures)
  - Seedable RNG for reproducible results
- Exportable to common formats (raw arrays, WAV, image patterns) — implementers can add exporters
- Small, modular API intended for use in scripts, apps, or the browser (if applicable)

## Getting started

### Prerequisites

- Node.js (v14+ recommended) if the project is JavaScript/TypeScript
- Or the appropriate runtime for the implementation contained in this repo

### Install

Clone the repository:

```bash
git clone https://github.com/harmfulladvocado/Noise-Generator.git
cd Noise-Generator
```

## Configuration / Options

Common options to support (suggested):

- type: string — 'white' | 'pink' | 'brown' | 'perlin' | 'simplex'
- seed: number | string — for deterministic noise
- sampleRate: number — audio sample rate (e.g., 44100)
- duration: number — duration in seconds for audio output
- amplitude: number — global amplitude multiplier (0.0–1.0)
- width / height / scale — for 2D noise textures

Adjust the options shape to fit your library's API.

## Examples

Include example scripts that demonstrate the project capabilities. Example folders to add to the repo:

- examples/audio-to-wav/ — generate and save a WAV file
- examples/texture/ — produce PNGs from Perlin/Simplex noise
- examples/benchmarks/ — demonstrate performance and memory usage

## Tests

Add unit tests covering:

- Each noise type produces expected statistical properties (e.g., mean ≈ 0 for white noise)
- Reproducibility when using the same seed
- Exporters produce valid outputs (WAV headers, image files, etc.)

```
