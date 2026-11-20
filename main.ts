// The World in One Picture — Friday 20 November 2026.
// Entry program for make.fun bounty news-image-20261120 (Node 22, stdlib only).
// It writes the repo's own news-summary image to the grader's output
// directory as entry.png: a whole 1024x1024 PNG, under 1 MiB, byte-identical
// on every run. Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// on every run, with no network and no other input.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
writeFileSync(target, readFileSync(join(here, "entry.png")));
