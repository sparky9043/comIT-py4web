# Django-Based Content Management Systems: django CMS & Wagtail

*A comprehensive overview and comparison — updated May 2026*

---

## Table of Contents

1. [What Is a CMS?](#what-is-a-cms)
2. [Why Django for a CMS?](#why-django-for-a-cms)
3. [django CMS](#django-cms)
   - [Background & History](#background--history)
   - [Latest Version: 5.x](#latest-version-5x)
   - [Key Features](#django-cms-key-features)
   - [Who Uses django CMS?](#who-uses-django-cms)
4. [Wagtail](#wagtail)
   - [Background & History](#background--history-1)
   - [Latest Version: 7.x](#latest-version-7x)
   - [Key Features](#wagtail-key-features)
   - [Who Uses Wagtail?](#who-uses-wagtail)
5. [Head-to-Head Comparison](#head-to-head-comparison)
6. [Which One Should You Choose?](#which-one-should-you-choose)

---

## What Is a CMS?

A **Content Management System (CMS)** is a software application that allows users to create, manage, and publish digital content — typically for the web — without needing to write code for every change. CMSes separate content from presentation, enabling non-technical editors to update a website while developers maintain the underlying architecture and templates.

CMSes broadly fall into a few categories:

- **Traditional / Coupled CMS:** The backend and frontend are tightly linked. The CMS serves fully rendered HTML pages (e.g., classic WordPress or Drupal).
- **Headless CMS:** The backend manages and exposes content via an API (REST or GraphQL), while the frontend is completely separate — built with React, Vue, Next.js, etc.
- **Hybrid CMS:** Supports both traditional page rendering and headless API delivery, giving teams flexibility to choose the approach per project.

Modern CMSes increasingly offer hybrid capability, as organizations demand omnichannel content delivery to websites, mobile apps, and third-party platforms simultaneously.

Other widely used open-source CMSes include WordPress (PHP), Drupal (PHP), Joomla (PHP), and Contentful (cloud-native headless). Django-based CMSes occupy a niche but prestigious corner of this space: they appeal to teams that are already invested in the Python/Django ecosystem and require a high degree of customization, security, and developer control.

---

## Why Django for a CMS?

[Django](https://www.djangoproject.com/) is a high-level Python web framework built on the "batteries included" philosophy. It ships with a powerful ORM, a built-in admin interface, robust authentication, an URL routing system, and strong security defaults. These properties make it an excellent foundation for a CMS:

- **Security:** Django's defaults protect against SQL injection, CSRF, XSS, and clickjacking out of the box.
- **Scalability:** Django powers high-traffic platforms like Instagram and Pinterest, proving it can handle enormous loads.
- **Customizability:** Content types, admin views, and data models are defined as plain Python code — no configuration language required.
- **Python ecosystem:** Access to pip packages for data science, machine learning, REST APIs, and more.
- **Active community:** Django has been in active development for over 20 years (it celebrated its 20th birthday in 2025).

The two most prominent Django CMSes are **django CMS** and **Wagtail**.

---

## django CMS

### Background & History

**django CMS** was originally developed by [Divio AG](https://www.divio.com/), a Swiss software agency, and first released publicly in 2009. For over a decade, Divio maintained the project as a flagship open-source effort alongside its commercial cloud-hosting platform.

In July 2020, Divio handed stewardship of the open-source project to the newly established **django CMS Association (dCA)**, a nonprofit body that now governs the project. Divio remains a sponsor and founding member, alongside other companies such as Eliga Services. This transition was intended to ensure the long-term independence and sustainability of the project under community governance.

The project went through several major milestones:

- **Version 3.x (2015–2023):** A long-running, stable series that established django CMS as a go-to enterprise CMS. v3.9 brought Django 3.2 LTS support.
- **Version 4.1 (December 31, 2023):** Marked the completion of a multi-year "enterprise-ready" initiative internally called "version 4," introducing revised model structures, major performance improvements, and dedicated edit/preview/structure endpoints.
- **Version 5.0 (May 2025):** A landmark release with headless support, security hardening, and a leaner backend. It skipped version 4.2 intentionally, using semantic versioning to signal the breadth of breaking changes from the v4 work.

### Latest Version: 5.x

As of early 2026, **django CMS 5.0.x** is the current Long-Term Support (LTS) release series. The latest patch release is **5.0.6**, with version 5.0.5 (November 2025) and 5.0.4 (October 2025) bringing multilingual fixes and performance improvements respectively. Version **5.1.0a1** is available as an alpha for testing.

**Compatibility:**
- Django: 4.2, 5.0, 5.1, and 5.2 (LTS supported through April 2028)
- Python: 3.10, 3.11, 3.12, and 3.13

**Headline changes in the 5.0 series:**

- **Full Headless Mode:** django CMS 5 can run with no exposed HTML page URLs at all. Content is delivered via the companion `djangocms-rest` package (reached stable 1.0 in late 2025), which provides a DRF-based REST API with typed endpoints and auto-generated OpenAPI schemas. A hybrid setup — serving some routes as HTML and others via API — is also supported.
- **Content Security Policy (CSP) compliance:** All inline JavaScript has been removed from edit mode. Communication with the frontend editor now uses `text/json` objects instead, allowing projects to enforce strict CSP headers and defend against XSS attacks.
- **Merged TreeNode + Page models:** The data model was simplified, merging formerly separate `TreeNode` and `Page` models, resulting in significant database query reductions.
- **Exception Handling Revamp:** Plugin rendering exceptions are now caught at the placeholder level, surfacing cleaner error messages and full stack traces in `DEBUG` mode.
- **Improved Placeholder Configuration:** `CMS_PLACEHOLDER_CONF` now works for any Django model, not only CMS pages.
- **`FrontendEditableMixin`:** Now standardized across all plugins, simplifying inline field editing.
- **Performance focus (5.0.3+):** Targeted optimizations to placeholder and plugin utilities improve editing speed on content-heavy pages with complex plugin hierarchies.
- **djangocms-versioning 2.2:** Bulk-delete for content versions, translation deletion from the language menu, and improved compatibility with django CMS 5.
- **djangocms-snippet 5.0:** Versionable universal snippet plugin compatible with both django CMS 3 and 4/5.
- **djangocms-alias 3.0:** Static aliases restored to the structure board, alongside enhanced security compliance features for enterprise deployments.

### django CMS Key Features

- **In-line / frontend editing:** Editors can click directly on page content to make changes, with the interface overlaid on the live page.
- **Plugin architecture:** Content is assembled from reusable plugins (text, image, video, form, alias, snippet, etc.). Plugins can be developed for any content type.
- **Structure Board:** A dedicated panel for managing the layout of placeholders and plugins on a page without entering edit mode.
- **Multilingual support:** Built-in handling of translated content across multiple languages; Transifex integration for the project's own UI translations.
- **Versioning:** Via the `djangocms-versioning` package, full version history with draft/published states, bulk operations, and translation management.
- **Multi-site support:** A single installation can host multiple websites.
- **Granular permissions:** Fine-grained access control at the page, placeholder, and plugin level.
- **SEO-friendly structure:** Hierarchical URL structure, meta-tag control, and sitemap generation.
- **Headless / hybrid:** Full headless mode via `djangocms-rest` (stable since late 2025), with REST API and OpenAPI schema support.
- **Enterprise-ready:** LTS releases with defined support windows aligned to Django LTS; used by large organizations.

### Who Uses django CMS?

django CMS is found primarily in enterprise, government, higher education, and B2B contexts. According to usage data from Enlyft, around 215 companies have been identified using django CMS, with 41% being large enterprises (over 1,000 employees) and usage concentrated in Information Technology & Services (14%), Computer Software (10%), and Higher Education (8%).

Notable sectors and organizations include:

- **Divio** — the original creator; uses django CMS as the foundation for its cloud hosting platform.
- **European institutions** — several EU-related organizations and governments rely on django CMS for multilingual, compliance-heavy sites.
- **Higher education** — universities in Europe and elsewhere use it for departmental and institutional websites.
- **Media companies** — the framework's plugin model is suited to structured editorial workflows.
- **Financial services** — security defaults and enterprise support have made it attractive to fintech and banking organizations.

django CMS is particularly popular in Germany, Switzerland, and the broader DACH region, reflecting its Swiss origins and the Divio ecosystem. The django CMS Association has growing membership from across Europe and beyond.

---

## Wagtail

### Background & History

**Wagtail** was created by [Torchbox](https://torchbox.com/), a UK-based digital agency whose mission centers on building technology for nonprofits and public-sector organizations. The CMS was originally built as a bespoke solution for the **Royal College of Art**, and the RCA's insistence that it be open-sourced led to Wagtail's public release in **2014**.

Torchbox retains a central role in the Wagtail ecosystem — they employ several core team members and provide commercial support, hosting, and development services. However, the project has grown into a genuine community effort, with 726 unique contributors tracked on GitHub by Wagtail's 10th anniversary in 2024.

Key milestones in Wagtail's history:

- **2014:** Open-sourced on GitHub.
- **2017:** The UK National Health Service (NHS) selects Wagtail to power NHS.uk, exposing it to massive scale (over 50 million visits per month).
- **2022:** Google provides $150,000 in corporate sponsorship for the development of Wagtail's next-generation page editor; Google had by that point been using Wagtail for several flagship properties, including blog.google.
- **2024:** Wagtail celebrates its 10th anniversary; headless usage surges (46% of surveyed projects report "most work is on headless," up from 24% in 2022).
- **2025:** Wagtail 7.0 released as an LTS, bringing Django 5.2 official support and autosave for draft content.

### Latest Version: 7.x

As of May 2026, **Wagtail 7.4 LTS** (released May 4, 2026) is the current long-term support release, supported until November 2027. **Wagtail 7.3** (February 2026) is in active support. The upcoming **Wagtail 8.0** is provisionally planned for August 2026.

Wagtail follows a predictable **quarterly release schedule** — new feature releases every three months, LTS releases roughly every 12 months.

**Compatibility (7.x):**
- Django: 4.2 and 5.2 (LTS)
- Python: 3.9+ (3.12/3.13 recommended)

**Headline changes across the 6.x–7.x generation:**

- **Wagtail 7.0 (May 2025, LTS):**
  - Official Django 5.2 compatibility.
  - **Draft autosave:** Required fields no longer block saving a draft — they are only enforced at publish time, paving the way for autosave workflows.
  - Foundation work for AI integration baked into the Wagtail backend.

- **Wagtail 6.4:**
  - **StreamField block previews:** Editors can see a visual preview of a block before committing to it.
  - **Drag-and-drop StreamField block reordering.**
  - Expanded headless CMS documentation and improvements.
  - Improved alt text capabilities for accessibility.

- **Wagtail 6.3 (LTS, November 2024):**
  - **Custom preview sizes:** Test content rendering at any device resolution, from small phones to 4K displays.
  - VPAT accessibility reporting format.

- **Wagtail 7.2 (November 2025):**
  - Fully revamped search functionality.
  - Readability checks for editors.

- **Wagtail 7.3 (February 2026):**
  - Further improvements from the February 2026 "What's New" release cycle.

- **Wagtail AI package:** Rather than bundling AI features into core, Wagtail maintains a separate `wagtail-ai` package, preserving optionality. This reflects a deliberate policy to support AI integration without mandating it.

### Wagtail Key Features

- **StreamField:** Wagtail's defining feature. Content is composed of typed, ordered blocks (RichText, Image, Embed, StructBlock, ListBlock, custom blocks, etc.) defined in Python models. This gives editors extreme flexibility while keeping content structured and semantically rich. Block previews (added in 6.4) let editors see exactly how each block will look before placing it.
- **Page tree model:** Content is organized in a hierarchical tree of typed pages. Each page type is a Django model subclass, giving developers full control over fields, validation, and routing.
- **Clean admin UI:** Widely praised for its editor-friendly interface. Wagtail deliberately targets both developer control and editorial ease-of-use.
- **Image management:** Built-in image library with focal-point cropping, responsive renditions, and alt-text management. Accessibility compliance for images was enhanced in 6.3.
- **Snippets:** Reusable, non-page content objects (e.g., team members, FAQs) that can be managed independently and embedded in pages.
- **Workflow and moderation:** Configurable multi-step editorial approval workflows with email notifications and audit trails.
- **Localization:** First-class support for multi-language and multi-site setups via `wagtail-localize`, compatible with translation memory systems.
- **Search:** Pluggable search backends (Elasticsearch, OpenSearch, or the built-in database backend). Version 7.2 shipped a fully revamped search experience.
- **Headless / API:** Wagtail provides a REST API out of the box (`wagtail.api`). Usage of headless mode has grown significantly, with 46% of surveyed projects reporting headless-primary usage.
- **Accessibility:** Strong commitment to accessibility for both the editor interface (WCAG-compliant admin) and output content (alt text tools, VPAT reporting).
- **Draft autosave (7.0+):** Incomplete drafts are saved automatically without requiring all required fields to be populated.

### Who Uses Wagtail?

Wagtail has an exceptionally high-profile user base relative to its niche position in the market. It is described as the world's most popular Django-based CMS, with tens of thousands of organizations worldwide using it. Notable users include:

- **Google** — Multiple flagship properties run on Wagtail, including `blog.google`, `about.google`, and `flutter.dev`. Google contributed $150,000 to Wagtail's development in 2022 and uses Wagtail because it meets Google's strict internal security standards.
- **NASA / Jet Propulsion Laboratory** — NASA.gov and the JPL website are powered by Wagtail. The JPL site was modernized on Wagtail specifically to handle mission updates, science news, images, and videos at scale.
- **UK National Health Service (NHS)** — NHS.uk, one of the highest-traffic government health portals in the world, runs on Wagtail. The site handles over 50 million visits per month and required Wagtail's scalability and content migration capabilities when it was first deployed in 2017.
- **Mozilla** — The makers of Firefox use Wagtail for internal and public sites.
- **Oxfam** — The international charity uses Wagtail for their global digital presence.
- **Salesforce** — Documentation and publishing sites at Salesforce leverage Wagtail.
- **NBC** — Media content management for NBC properties.
- **BMW** — Automotive marketing content managed via Wagtail.
- **MIT** — The Massachusetts Institute of Technology uses Wagtail for institutional sites.
- **Red Cross** — The charity's digital estate includes Wagtail-powered properties.
- **Amnesty International** — Rights organization uses Wagtail for global campaigns.
- **eBay** — Has used Wagtail for content sites.
- **Peace Corps (USA)** — Modernized its communications platform with Wagtail.
- **Children's Health Ireland** — Consolidated five disparate websites into one Wagtail site.
- **US and UK government sites** — `usa.gov` and various UK government services.
- **Twilio / SendGrid** — Documentation properties.

---

## Head-to-Head Comparison

| Feature | django CMS 5.x | Wagtail 7.x |
|---|---|---|
| **First release** | 2009 | 2014 |
| **Latest stable** | 5.0.6 (LTS) | 7.4 LTS |
| **License** | BSD | BSD |
| **Python support** | 3.10 – 3.13 | 3.9+ |
| **Django support** | 4.2, 5.0, 5.1, 5.2 | 4.2, 5.2 |
| **Content model** | Plugin-based placeholders on pages | Typed page models with StreamField blocks |
| **Inline / frontend editing** | Yes — click-to-edit overlaid on live page | Limited (admin-based editing; no live frontend overlay by default) |
| **Structure Board** | Yes (dedicated drag-and-drop layout view) | No direct equivalent; admin-based structure |
| **Headless support** | Full headless mode + djangocms-rest 1.0 (stable) | REST API included; strong headless ecosystem |
| **Versioning** | Via djangocms-versioning (bulk ops, drafts, translations) | Built-in draft/live states; revision history |
| **Workflow / approval** | Basic (via plugins / association packages) | Configurable multi-step moderation workflows built-in |
| **Multilingual** | First-class, built into core | Via wagtail-localize (external but official package) |
| **Multi-site** | Built-in | Built-in |
| **SEO tooling** | Core page meta tools + third-party packages | SEO fields on pages; improvements on the 2025–2026 roadmap |
| **Admin UI style** | Django admin-like, structured, functional | Custom, clean, editor-friendly UI widely praised for UX |
| **Ease of use for editors** | Moderate — powerful but complex | High — frequently cited as best-in-class editor UX |
| **Developer flexibility** | High — plugins, custom apps, rich configuration | Very high — full Django model control; StreamField extensibility |
| **AI integration** | Community packages; growing interest | Separate `wagtail-ai` package (opt-in by design) |
| **Accessibility** | Standard Django/HTML practices | Strong commitment; WCAG-compliant admin, VPAT reports, alt text tools |
| **Release cadence** | As-needed; LTS aligned to Django LTS | Quarterly feature releases; LTS ~annually |
| **Governance** | django CMS Association (nonprofit) | Torchbox + community contributors |
| **Commercial support** | Divio, Eliga, dCA member agencies | Torchbox (creators), plus ecosystem partners |
| **GitHub stars (approx.)** | ~10,000 | ~18,000+ |
| **Primary geography** | Strong in Europe (esp. DACH region) | Global, strong in UK, US, Australia |
| **Typical adopters** | Enterprise, government, higher ed, B2B | Media, NGO, government, large tech companies |

### Content Architecture

These two CMSes approach content structure fundamentally differently, and this is the most important decision axis:

**django CMS** uses a **placeholder + plugin model**. Pages have pre-defined placeholder slots (defined in templates), and editors fill those slots with plugins — reusable content units. This makes page assembly very visual and modular, and the Structure Board gives a bird's-eye view of the layout. It excels when your pages need flexible, drag-and-drop assembly from a library of components.

**Wagtail** uses a **typed page model + StreamField model**. Each page type is a Django model with explicit fields. The flexible content area, if any, is a `StreamField` — an ordered sequence of typed blocks. This approach keeps content semantically rich and queryable, makes API delivery cleaner, and is well-suited to structured editorial workflows. It trades some of the freeform layout flexibility of the plugin model for better content integrity and portability.

### Editor Experience

Wagtail consistently receives higher marks from content editors for day-to-day usability. Its admin UI is a fully custom, thoughtfully designed interface — not the standard Django admin skin. Features like preview modes, custom preview sizes, autosave, and the StreamField block previewer make editorial work smooth.

django CMS's frontend editing mode — where you click on live page content to edit it inline — can be compelling for certain use cases, particularly for marketing teams who want to see changes in context. However, the learning curve around the plugin/placeholder model can be steeper for less technical editors.

### Headless and API Delivery

Both CMSes have reached strong headless maturity as of 2025–2026:

- **django CMS** achieved full headless parity in 5.0, with `djangocms-rest` 1.0 completing the story with a stable, production-ready REST API. A hybrid setup (some routes as HTML, others as API) is explicitly supported.
- **Wagtail** has offered a REST API since early versions (`wagtail.api`), and headless adoption has grown dramatically — nearly half of surveyed users reported primarily headless usage in 2024. Wagtail's typed page/field model makes API responses clean and predictable.

### Community and Ecosystem

Wagtail has the larger community by most metrics — more GitHub stars, a broader international contributor base, and higher-profile public-sector endorsements. The `wagtail.org` showcase includes some of the world's most-visited institutional websites.

django CMS has a stable, European-centric ecosystem with strong enterprise and agency support, particularly from the Divio ecosystem and the dCA's growing member network. It has approximately 39 pull requests merged per month as of early 2025 and a committed core team.

---

## Which One Should You Choose?

**Choose django CMS if:**

- Your editors prefer visual, in-context frontend editing (clicking on live page content to edit it).
- Your site architecture is primarily page-based with flexible layout requirements (many different component types per page).
- You need enterprise versioning with bulk operations, granular permissions, and multilingual support all in one package.
- Your team is in the European/DACH ecosystem and can benefit from proximity to the dCA and Divio support network.
- You want a CMS that has been battle-tested in enterprise deployments since 2009, with a clear LTS support window.

**Choose Wagtail if:**

- Editor experience and clean UI are high priorities — Wagtail's admin is widely regarded as the gold standard.
- Your content structure benefits from strong typing — blog posts, news articles, case studies, events, products with distinct field schemas.
- You're building for organizations like media, public sector, NGOs, or large charities, where Wagtail has the deepest track record.
- You want headless-first or hybrid delivery with clean, structured API output.
- You need a quarterly innovation cadence with a predictable LTS cycle.
- You need to scale to tens of millions of monthly visits — Wagtail's track record at the NHS, NASA, and Google demonstrates this capability.

**In either case:** both CMSes are mature, actively maintained, BSD-licensed, and built for the long term. The choice ultimately comes down to your content model, your editors' needs, and the kind of customization and ecosystem support your team values most.

---

*Sources: django CMS official blog and documentation (django-cms.org/docs.django-cms.org), Wagtail official blog and documentation (wagtail.org), Torchbox case studies, G2 reviews, and Wagtail/django CMS GitHub repositories.*
