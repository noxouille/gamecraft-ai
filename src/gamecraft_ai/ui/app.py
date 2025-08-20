import gradio as gr

from ..services.llm import LLMService
from .handlers import UIHandlers


def create_gradio_app() -> gr.Blocks:
    """Create the main Gradio application interface"""

    # Initialize handlers
    ui_handlers = UIHandlers()

    # Custom CSS for better styling
    css = """
    .container {
        max-width: 1200px;
        margin: auto;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .example-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    """

    with gr.Blocks(css=css, title="GameCraft AI", theme=gr.themes.Soft()) as app:
        # Header
        with gr.Row(elem_classes="header"):
            gr.Markdown(
                """
            # 🎮 GameCraft AI
            ### AI-Powered YouTube Video Summary & Script Generator
            Generate professional gaming content scripts from simple queries in English or French.
            """
            )

        # Main interface
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("## 📝 Input")

                query_input = gr.Textbox(
                    label="Query",
                    placeholder="Example: Make a 10-minute review video about Baldur's Gate 3",
                    lines=3,
                    max_lines=5,
                )

                duration_slider = gr.Slider(
                    minimum=5, maximum=20, value=10, step=1, label="Duration (minutes)"
                )

                # Model selection dropdown
                available_models = LLMService.get_available_models()
                model_choices = []
                model_labels = {}

                for model_id, model_info in available_models.items():
                    label = f"{model_info['name']} - {model_info['description']}"
                    model_choices.append((label, model_id))
                    model_labels[model_id] = label

                model_dropdown = gr.Dropdown(
                    choices=model_choices,
                    value="gpt-4o-mini",
                    label="🤖 AI Model",
                    info="Select the AI model for processing",
                )

                process_btn = gr.Button("🚀 Generate Script", variant="primary", size="lg")

                # Examples section
                gr.Markdown("### 💡 Example Queries")
                with gr.Row():
                    examples = [
                        ["Make a 10-minute review video about Baldur's Gate 3", 10],
                        ["Create a 15-minute preview of Starfield", 15],
                        ["Fais une critique de 10 minutes de Spider-Man 2", 10],
                        ["Make a summary of Xbox Showcase https://youtube.com/watch?v=example", 12],
                    ]

                    gr.Examples(
                        examples=examples,
                        inputs=[query_input, duration_slider],
                        label="Click to try:",
                    )

        # Output section
        gr.Markdown("## 📄 Generated Content")

        with gr.Tab("📜 Script"):
            script_output = gr.Markdown(
                value="Your generated script will appear here...", label="Generated Script"
            )

        with gr.Tab("🔍 Research Data"):
            research_output = gr.Markdown(
                value="Game information and research data will appear here...",
                label="Research Data",
            )

        with gr.Tab("🎥 YouTube Links"):
            youtube_output = gr.Markdown(
                value="Video footage links will appear here...", label="YouTube Video Links"
            )

        with gr.Tab("🖼️ Thumbnail Ideas"):
            thumbnail_output = gr.Markdown(
                value="Viral thumbnail suggestions will appear here...",
                label="Thumbnail Suggestions",
            )

        # Progress indicator
        with gr.Row():
            status_text = gr.Textbox(
                label="Status", value="Ready to process your query...", interactive=False
            )

        # Event handlers
        def update_status(query, duration, model):
            if not query.strip():
                return "Please enter a query..."
            model_name = available_models[model]["name"]
            return f"Processing: '{query[:50]}...' ({duration} min) using {model_name} - This may take up to 60 seconds..."

        def process_and_update(query, duration, model):
            try:
                script, research, youtube_links, thumbnail_ideas = ui_handlers.process_query(
                    query, duration, model
                )
                status = "✅ Processing complete!"
                return script, research, youtube_links, thumbnail_ideas, status
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                return error_msg, "", "", "", error_msg

        # Wire up the interface
        process_btn.click(
            fn=update_status,
            inputs=[query_input, duration_slider, model_dropdown],
            outputs=[status_text],
            queue=False,
        ).then(
            fn=process_and_update,
            inputs=[query_input, duration_slider, model_dropdown],
            outputs=[script_output, research_output, youtube_output, thumbnail_output, status_text],
        )

        # Footer
        gr.Markdown(
            """
        ---
        ### 🚀 Features
        - **Dual Mode**: Event summaries or game reviews
        - **Bilingual**: English and French support
        - **Smart Research**: Automatic game info, media, and review aggregation
        - **Multiple Formats**: Review, preview, complete guide templates
        - **Fast Processing**: Results in under 60 seconds

        *Built with LangGraph, Gradio, and Pydantic*
        """
        )

    return app


if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
