# Unofficial Onyx SDK Docs

https://github.com/progressive-kiwi/onyx-inking-unofficial-docs

**Deployed site:** https://progressive-kiwi.github.io/onyx-inking-unofficial-docs/

Unofficial documentation for the Onyx BOOX e-ink Android SDK, covering the
`onyxsdk-pen`, `onyxsdk-base`, and `onyxsdk-device` modules.

> **Note:** This documentation is AI-generated from reverse-engineering the SDK
> AARs, debug session logs, and open-source reference apps. It is not affiliated
> with or endorsed by Onyx International.

## Building the docs

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run sphinx-autobuild docs docs/_build/html --port 8000
```

## Note to Onyx International

If anyone from Onyx is reading this — I'd be more than happy to deprecate this
in favour of official documentation. Please reach out!

## License

MIT
