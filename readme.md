Prometheus exporter for [Poste.io](https://poste.io/) mailserver. \
Exposes in/out stats by domain and mailbox at `IP:8080` \
Running in Portainer require ENV variables must be specified without quotes.

For example, this rule will fire if any mailbox sends over 100 emails in 1 hour:

Grafana alerting rule can be configured like this(replace *mailserver_name* with yours): \
create expression A (type: prometheus): \
&emsp;&emsp;time range: now-2h to now-1h \
&emsp;&emsp;query: *mailserver_name*_mailbox_out{} \
&emsp;&emsp;legend: {{mailbox}} \
create expression B (type: prometheus): \
&emsp;&emsp;time range: now-1h to now \
&emsp;&emsp;query: *mailserver_name*_mailbox_out{} \
&emsp;&emsp;legend: {{mailbox}} \
create expression C (type: math), also alert condition: \
&emsp;&emsp;expression: $B-$A>100 

At step 3. Set evaluation behavior: \
&emsp;&emsp;set "Alert state if no data or all values are null" to "OK" to avoid false positive.

Also, you can add one more service - [auto password changer](https://github.com/dtkbrbq/poste_pass_changer) to automatically change password of suspicious mailbox.
