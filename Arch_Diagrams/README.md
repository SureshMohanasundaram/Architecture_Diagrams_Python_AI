# Arch_Diagrams: AWS Microservices Example

This folder contains an example architecture diagram for a typical
microservices platform on AWS including Spring Boot services on EKS,
Amazon MSK (Kafka), Terraform for IaC, GitLab for CI/CD, and JFrog
Artifactory for artifact storage.

Files added:
- `diagrams/aws_microservices.dot` - GraphViz DOT description of the architecture
- `render_aws_microservices.py` - helper to render the DOT to an image (PNG by default)

Rendering instructions

1) Ensure Graphviz is installed on your machine and `dot` is on PATH.
   Windows: install from https://graphviz.org/download/ and add `C:\Program Files\Graphviz\bin` to PATH.

2) (Optional) Activate your Python virtualenv and install Python deps:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3) Render the diagram using the helper script:

```powershell
python .\render_aws_microservices.py
# or to render as SVG:
python .\render_aws_microservices.py svg
```

4) Alternatively, use the Graphviz `dot` command directly:

```powershell
dot -Tpng .\diagrams\aws_microservices.dot -o .\diagrams\aws_microservices.png
```

Next steps
- If you want a `diagrams` (Python) version using the `diagrams` library, I can add `Arch_Diagrams/aws_microservices.py` that produces a similar visual using AWS icons.
- I can also attempt to render the PNG here if you want and allow me to run the renderer in this environment (I may need Graphviz installed on the system first).
