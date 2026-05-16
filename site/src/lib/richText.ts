import katex from "katex";

type RichTextPart = {
  kind: "text" | "math";
  value: string;
};

const KATEX_OPTIONS: katex.KatexOptions = {
  throwOnError: false,
  strict: "ignore",
  output: "mathml",
  trust: false,
  macros: {
    "\\vect": "\\mathbf{#1}",
  },
};

const KATEX_DISPLAY_OPTIONS: katex.KatexOptions = {
  ...KATEX_OPTIONS,
  displayMode: true,
};

export function renderRichText(value: string): string {
  return splitInlineMath(value)
    .map((part) => (part.kind === "math" ? renderInlineMath(part.value) : escapeHtml(part.value)))
    .join("");
}

export function renderDisplayMath(value: string): string {
  const normalized = normalizeDisplayMath(value);
  if (!normalized) {
    return "";
  }
  return katex.renderToString(normalized, KATEX_DISPLAY_OPTIONS);
}

function renderInlineMath(value: string): string {
  const normalized = normalizeInlineMath(value);
  if (!normalized) {
    return "";
  }
  return katex.renderToString(normalized, KATEX_OPTIONS);
}

function normalizeDisplayMath(value: string): string {
  let normalized = value
    .replace(/\\label\{[^}]+\}/g, "")
    .replace(/\\notag\b/g, "")
    .trim();
  const environment = normalized.match(/^\\begin\{([^}]+)\}([\s\S]*)\\end\{\1\}$/);
  if (environment) {
    const [, name, body] = environment;
    const bodyMath = normalizeInlineMath(body);
    if (name === "align" || name === "align*") {
      return `\\begin{aligned}${bodyMath}\\end{aligned}`;
    }
    return bodyMath;
  }
  return normalizeInlineMath(normalized);
}

function normalizeInlineMath(value: string): string {
  return value
    .replace(/\$/g, "")
    .replace(/((?:\\(?!text\b)[A-Za-z]+)|^|[^A-Za-z0-9{.])(\d+(?:\.\d+)?e[+-]\d+)/g, "$1\\text{$2}")
    .replace(/\\num\{([^{}]+)\}/g, "$1")
    .replace(/\\inR(?=[^A-Za-z]|$)/g, "\\in\\mathbb{R}")
    .replace(/\\inZ(?=[^A-Za-z]|$)/g, "\\in\\mathbb{Z}")
    .replace(/\\top(?=[A-Za-z])/g, "\\top ")
    .replace(/\\textbf\{([A-Za-z]+)_([A-Za-z0-9]+)\}/g, "\\mathbf{$1}_{$2}")
    .replace(/\\slash/g, "/")
    .trim();
}

function splitInlineMath(value: string): RichTextPart[] {
  const parts: RichTextPart[] = [];
  let textStart = 0;
  let mathStart: number | null = null;
  let braceDepth = 0;
  let escaped = false;

  for (let index = 0; index < value.length; index += 1) {
    const char = value[index];
    if (char === "\\" && !escaped) {
      escaped = true;
      continue;
    }
    if (mathStart !== null && !escaped) {
      if (char === "{") {
        braceDepth += 1;
      } else if (char === "}" && braceDepth > 0) {
        braceDepth -= 1;
      }
    }
    if (char === "$" && !escaped) {
      if (mathStart === null) {
        if (textStart < index) {
          parts.push({ kind: "text", value: value.slice(textStart, index) });
        }
        mathStart = index + 1;
        braceDepth = 0;
      } else if (braceDepth === 0) {
        parts.push({ kind: "math", value: value.slice(mathStart, index) });
        mathStart = null;
        textStart = index + 1;
      }
    }
    escaped = false;
  }

  if (mathStart !== null) {
    parts.push({ kind: "text", value: value.slice(textStart) });
  } else if (textStart < value.length) {
    parts.push({ kind: "text", value: value.slice(textStart) });
  }
  return parts;
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
