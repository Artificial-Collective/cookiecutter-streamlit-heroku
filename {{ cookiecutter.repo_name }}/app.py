from hydralit import HydraApp
from src import apps
import yaml
from src.utils.utils import get_config, dotenv_loader


def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


if __name__ == '__main__':
    dotenv_loader()
    config = get_config()
    over_theme = {'txc_inactive': '#FFFFFF'}
    app = HydraApp(
        title='{{ cookiecutter.project_name }}',
        nav_horizontal=True,
        hide_streamlit_markers=False,
        use_navbar=True,
        use_loader=False,
        navbar_sticky=True,
        navbar_animation=False,
        navbar_theme=over_theme,
    )
    app_list = [
        ('Example', apps.ExampleApp),
    ]
    for app_name, app_cls in app_list:
        app.add_app(app_name, app_cls(config))

    app.add_app("Logout", apps.LoginApp(), is_login=True)

    app.add_loader_app(apps.LoaderApp(delay=0))
    user_access_level, username = app.check_access()

    if user_access_level == 2:
        complex_nav = {
            'Example': ['Example'],
        }
    elif user_access_level == 1:
        complex_nav = {
            'Example': ['Example'],
        }
    elif user_access_level == 3:
        complex_nav = {
            'Example': ['Example'],
        }
    else:
        complex_nav = {}
    app.run(complex_nav)
