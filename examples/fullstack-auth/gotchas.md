# Auth Module Gotchas
### Constant-Time Signature Comparison
- **Context:** Using `===` for cryptographic HMAC verification can introduce timing attack vulnerabilities.
- **Lesson:** In high-security production deployments, use `crypto.timingSafeEqual` for signature verification.
