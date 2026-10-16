# Responsible-use notes

Age and gender classifiers infer patterns from pixels; they do not know an individual's actual age, gender identity, or sex. Their performance can vary materially across lighting, image quality, race, ethnicity, age, presentation, disability, and other characteristics.

- Show results as estimates with confidence, as this UI does.
- Obtain consent before processing images of people.
- Do not store submitted frames by default; this server keeps uploads in memory only.
- Do not use predictions to make decisions about employment, education, housing, insurance, credit, public benefits, law enforcement, security screening, or access to services.
- Do not present the binary model labels as a person's identity. The UI calls them perceived gender presentation for this reason.

Before any production use, complete a domain-specific privacy, bias, and security review.
