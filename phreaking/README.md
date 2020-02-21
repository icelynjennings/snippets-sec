# Emails

## Preventing e-mails from being spoofed, from being marked as spam

### [SPF](http://www.openspf.org/FAQ) (Sender Policy Framework)

An email-validation system. It detects email spoofing via allowing receiving mail exchangers to check that incoming mail comes from a host authorised by its domain's administrators. IMPORTANT: Max 10 DNS records per domain, if it reads more, it breaks to avoid DNS amplification attacks.

### [DKIM](http://www.dkim.org/) (DomainKeys Identified Mail) 

Validates a domain name identity that associated with a message through cryptographic authentication.

### [DMARC](https://dmarc.org/).

Email authentication, policy, and reporting protocol on top of SPF and DKIM.

Adds extra features such as published policies to deal with non-compliant e-mail, linkage with
the From: field on an e-mail, etc.

- dmarcian.com

### SPF Flattener

Reduces the amount of DNS lookups to less than 10. Periodically looks at all the domains included in the record, their IP addresses and adds them to a SPF TXT record instead. This allows to set your DMARC policy to quarantine, so any email that fails DMARC (i.e fails SPF or DKIM) is marked as spam.

SPF can be automatically configured by Route53 with an SPF Flattener - each new entry is overridden by the flatter the next time it runs.
