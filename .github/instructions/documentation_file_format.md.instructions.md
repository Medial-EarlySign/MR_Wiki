---
applyTo: '**'
---

## Documentation Agent Instructions

Your primary task is to generate or modify MkDocs-compatible Markdown documentation. Adhere to the following output and content guidelines:

### Output Format

1. **Markdown and MkDocs Compatibility:**
    - Ensure all documentation is in **Markdown format**, compatible with MkDocs.
    - Use appropriate Markdown syntax for headings, lists, links, and code blocks.
    - Use **four spaces** for indentation within nested lists only (to comply with MkDocs parsing). Standard lists should not use this extra indentation.
    - Maintain an **empty line** between regular text and lists for clarity.

### Documentation Structure and Content

2. **Structural Improvement**: You are empowered to e**dit existing files** or **create/propose multiple new Markdown files** if doing so results in a more logical, comprehensive, and user-friendly documentation structure.
3. **Clarity and Practicality**: **Rephrase all content** to be as clear, concise, and practical for the end-user as possible. Prioritize actionable guidance and simple explanations.
4. **Gap Identification**: If any necessary information, examples, or sections are missing from the content you are generating or editing, insert a clear placeholder tag: `@@@[PLEASE_COMPLETE]` or an equivalent specific instruction to the human author.

### Review and Summary (Mandatory)

5. **Post-Generation Report**: After completing the documentation files, you **must** provide a final summary in the chat, including:
    * An **explanation** of why your proposed/modified file structure is superior to the previous one (or why the new structure is the most logical).
    * A **list of gaps or missing items** that need to be addressed by a human author, based on the `@@@[PLEASE_COMPLETE]` tags you inserted.
    * A Summary why this documentation is now more clear, concise, and practical for the end-user.
    * Any **additional suggestions** for further improvement or enhancement of the documentation.
