{{- define "api.name" -}}
{{ .Release.Name }}-api
{{- end }}

{{- define "api.labels" -}}
app: {{ include "api.name" . }}
release: {{ .Release.Name }}
{{- end }}
