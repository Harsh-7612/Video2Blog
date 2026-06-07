# Contributing to Vid2Blog

We love contributions! If you want to help make YouTube-to-blog conversions faster and more accurate, please follow these steps:

## How to Contribute
1. Fork the repo and create a branch (`feature/add-local-whisper-support`).
2. Ensure you handle YouTube download exceptions gracefully, as platform changes frequently break extractors.
3. Keep the `blog_generator.py` prompts abstracted so users can easily swap out the default blog style.
4. Submit a Pull Request detailing your changes.

**Note:** Please do not commit any downloaded `.mp4` or `.mp3` files to the repository.
