{{- define "frontend.name" -}}
{{ .Release.Name }}-frontend
{{- end }}

{{- define "frontend.labels" -}}
app: {{ include "frontend.name" . }}
release: {{ .Release.Name }}
{{- end }}
