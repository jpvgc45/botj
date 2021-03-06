from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from demo import config
import os


logger = logging.getLogger()  # get the root logger


def run_widget():
    import os
    from rasa_core.agent import Agent
    from rasa_addons.webchat import WebChatInput, SocketInputChannel

    agent = Agent.load('models/dialogue/',
                       interpreter='models/nlu/current/')
    input_channel = WebChatInput(static_assets_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static'))
    agent.handle_channel(SocketInputChannel(5500, "/", input_channel))


def run_remote():
    from rasa_core.remote import RemoteAgent

    logging.basicConfig(level="DEBUG")

    from rasa_extensions.core.channels.rasa_chat import RasaChatInput
    from rasa_addons.webchat import WebChatInput, SocketInputChannel

    rasa_in = RasaChatInput(config.platform_api)
    widget_in = WebChatInput(static_assets_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static'))
    input_channel = SocketInputChannel(config.self_port, "/",
                                       rasa_in, widget_in)

    agent = RemoteAgent.load(config.core_model_dir,
                             config.remote_core_endpoint,
                             config.rasa_core_token
                             )

    agent.handle_channel(input_channel)


if __name__ == "__main__":

    run_remote()
