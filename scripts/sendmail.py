import modules.scripts as scripts
import gradio as gr

from modules import ui_components
from modules.processing import Processed, StableDiffusionProcessing
from scripts.sendmail_core import StmtMail

class ExtensionTemplateScript(scripts.Script):
        def title(self):
                return "SendMail"

        def show(self, is_img2img):
                return scripts.AlwaysVisible

        def ui(self, is_img2img):
                with ui_components.InputAccordion(False, label="SendMail") as enable:
                        with gr.Row():
                                smtp = gr.Textbox(
                                        placeholder="smtp.domain.com",
                                        label="SMTP host"
                                )
                                port = gr.Textbox(
                                        value="587",
                                        placeholder="25, 465, 587, 2525",
                                        label="Port"
                                )
                        with gr.Row():
                                id = gr.Textbox(
                                        type="email",
                                        placeholder="postmaster@domain.com",
                                        label="SenderID"
                                )
                                pw = gr.Textbox(
                                        type="password",
                                        label="SenderPW"
                                )
                        with gr.Row():
                                to_user = gr.Textbox(
                                        placeholder="to@domain.com",
                                        label="To"
                                )
                        with gr.Row():
                                subject = gr.Textbox(
                                        value="[SD] Ended img2img",
                                        label="Subject"
                                )
                        with gr.Row():
                                contents = gr.TextArea(
                                        value="Ended img2img",
                                        label="Contents"
                                )
                return [enable, smtp, port, id, pw, to_user, subject, contents]

        def process(self, p, enable, smtp, port, id, pw, to_user, subject, contents):
                self.enable = enable
                self.smtp = smtp
                self.port = port
                self.sendmail_id = id
                self.sendmail_pw = pw
                self.to_user = to_user
                self.subject = subject
                self.contents = contents

        def postprocess(self, p: StableDiffusionProcessing, processed: Processed, *args):
                if self.enable:
                        information = f"\n\nSteps: {processed.steps}, Sampler: {processed.sampler_name}, CFG scale: {processed.cfg_scale}, Seed: {processed.seed}, Model hash: {processed.sd_model_hash}, Model: {processed.sd_model_name}, Denoising strength: {processed.denoising_strength}, Version: {processed.version}"
                        StmtMail(STMT_HOST=self.smtp, PORT=self.port, ID=self.sendmail_id, PW=self.sendmail_pw).sendmail(
                                to_user=self.to_user,
                                subject=self.subject,
                                contents=self.contents + information
                        )