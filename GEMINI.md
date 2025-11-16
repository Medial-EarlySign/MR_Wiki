# Project: Documentation Wiki of MES Framework

## Documentation Agent Instructions

Your primary task is to generate or modify MkDocs-compatible Markdown documentation. Adhere strictly to the following output, content, and review guidelines.

---

### Output Format (Strict Technical Requirements)

1. **MkDocs & Markdown Compliance:**
    - All generated content **must** be in valid **Markdown format**.
    - **Indentation Rule:** Use **four spaces** for indentation ONLY within nested lists (lists within lists) to ensure MkDocs compatibility. Do not use this indentation for standard, top-level lists.
    - **Spacing Rule:** Maintain a single **empty line** between regular prose/text and any subsequent list (bulleted or numbered) for optimal readability and parsing.
2. **Output Directory and File Placement:**
    * Place all generated or modified files under the main documentation path: `MR_WIKI`.
    * Ensure files are placed logically into the correct subdirectories within `MR_WIKI`.
    * **ABSOLUTELY DO NOT** place Markdown documentation files inside application code directories. All documentation belongs under the `MR_WIKI` path.
3. **Internal Linking Policy:**
    * **Preserve Links:** You **must not remove** any existing internal or external links in the content unless specifically instructed.
    * **Suggested Removal Tag:** If you identify a link that appears unnecessary or irrelevant, you must mark it clearly using the tag: `@@@[SUGGEST_REMOVE_LINK]`.

---

### Documentation Structure and Content

1. **Structural Authority:** You are fully empowered to **edit existing files** or **propose/create multiple new Markdown files** if, and only if, this results in a more logical, comprehensive, and superior user experience and documentation structure.
2. **Clarity and Tone:** **Rephrase all content** to maximize clarity, conciseness, and practicality for the end-user. Prioritize actionable steps, simple explanations, and a professional, helpful tone.
3. **Gap Identification Tag:** If any necessary information, examples, code snippets, or crucial sections are missing from the content you are generating or editing, insert the clear placeholder tag: `@@@[PLEASE_COMPLETE_MISSING_INFO]`.

---

### Review and Summary (Mandatory Report)

Upon completion of the documentation generation/modification task, you **must** provide a final summary in the chat based on the following criteria:

1. **Structure Justification:** Provide a clear **explanation** of why the proposed/modified file structure is superior (or why the new structure is the most logical choice) for the end-user.
2. **Required Human Actions:** Provide a **list of all content gaps** that require human author intervention, based on the `@@@[PLEASE_COMPLETE_MISSING_INFO]` tags you inserted.
3. **Content Improvement Summary:** Summarize how this documentation is now more clear, concise, and practical for the end-user, referencing the content changes made.
4. **Further Suggestions:** List any **additional suggestions** for future enhancement, tooling improvements, or expansion of the documentation effort.