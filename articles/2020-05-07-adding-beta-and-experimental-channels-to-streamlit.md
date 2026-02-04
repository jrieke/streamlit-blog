---
title: "Adding Beta and Experimental \u201cChannels\u201d to Streamlit"
subtitle: "Introducing the st.beta and st.experimental namespaces"
date: 2020-05-07
authors:
  - "TC Ricks"
category: "Product"
---

![Adding beta and experimental “channels” to Streamlit](https://streamlit.ghost.io/content/images/size/w2000/2022/08/image--10-.svg)


Hey community 👋,

At Streamlit, we like to move fast while keeping things stable. And in our latest effort to move even faster while keeping the promise of stability, [we’re introducing the](https://docs.streamlit.io/en/latest/pre_release_features.html?ref=streamlit.ghost.io) `st.beta` [and](https://docs.streamlit.io/en/latest/pre_release_features.html?ref=streamlit.ghost.io) `st.experimental` [namespaces](https://docs.streamlit.io/en/latest/pre_release_features.html?ref=streamlit.ghost.io). These are basically prefixes we attach to our function names to make sure their status is clear to everyone.

Here’s a quick rundown of what you get from each namespace:

* ****st****: this is where our core features like `st.write` and `st.dataframe` live. If we ever make backward-incompatible changes to these, they will take place gradually and with months of announcements and warnings.
* ****st.beta****: this is where all new features land before they find their way to `st`. This gives you a chance to try the next big thing we’re cooking up weeks or months before we’re ready to stabilize its API.
* ****st.experimental****: this is where we’ll put features that may or may not ever make it into `st`. We don’t know whether these features have a future, but we want you to have access to everything we’re trying, and work with us to figure them out.

The main difference between st.beta and st.experimental is that beta features are expected to make it into the st namespace at some point soon, while experimental features may never make it.

More details below.

# Beta

Features in the beta namespace are all scheduled to become part of `st`, or core Streamlit. While in beta, a feature’s API and behaviors may not be stable, and it’s possible they could change in ways that aren’t backward-compatible.

****The lifecycle of a beta feature****

1. A feature is added to the beta namespace.
2. The feature’s API stabilizes and the feature is **cloned** into the `st` namespace, so it exists in both `st` and `st.beta`. At this point, users will see a warning when using the version of the feature that lives in the beta namespace – but the `st.beta` feature will still work.
3. At some point, the feature is **removed** from the `st.beta` namespace, but there will still be a stub in `st.beta` that shows an error with appropriate instructions.
4. Finally, at a later date the stub in `st.beta` is removed.

****Keeping up-to-date with beta features****

* All Beta features will be announced in the changelogs.
* All Beta features will show up in our documentation alongside normal features. For example, `st.beta_color_picker()` will be documented on the same page as `st.slider()`.

# Experimental

Features in the experimental namespace are things that we’re still working on or trying to understand. If these features are successful, at some point they’ll become part of core Streamlit, by moving to the `st.beta` namespace and then to `st`. If unsuccessful, these features are removed without much notice.

****Note:**** Experimental features and their APIs may change or be removed at any time.

****The lifecycle of an experimental feature****

1. A feature is added to the experimental namespace.
2. The feature is potentially tweaked over time, with possible API/behavior breakages.
3. At some point, we either move the feature into `st.beta` or remove it from `st.experimental`. Either way, we leave a stub in `st.experimental` that shows an error with instructions.

****Keeping up-to-date with experimental features****

* All Experimental features will be announced in the changelogs.
* All Experimental features will show up in a separate section of the API page in the docs, called “experimental features” (not created yet!)

Let us know if you have any questions or feedback about the new namespaces!
