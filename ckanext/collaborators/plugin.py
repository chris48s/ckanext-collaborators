import logging

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckanext.collaborators import blueprint

from ckanext.collaborators.helpers import get_collaborators
from ckanext.collaborators.model import tables_exist
from ckanext.collaborators.logic import action, auth

from ckanext.collaborators.views.package import collaborators, collaborator_delete, CollaboratorEditView

log = logging.getLogger(__name__)


class CollaboratorsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IBlueprint)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        if not tables_exist():
            log.critical(u'''
The dataset collaborators extension requires a database setup. Please run the following
to create the database tables:
    paster --plugin=ckanext-collaborators collaborators init-db
''')
        else:
            log.debug(u'Dataset collaborators tables exist')

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'collaborators')

    # IActions
    def get_actions(self):
        return {
            'dataset_collaborator_create': action.dataset_collaborator_create,
            'dataset_collaborator_delete': action.dataset_collaborator_delete,
            'dataset_collaborator_list': action.dataset_collaborator_list,
        }

    # IAuthFunctions
    def get_auth_functions(self):
        return {
            'dataset_collaborator_create': auth.dataset_collaborator_create,
            'dataset_collaborator_delete': auth.dataset_collaborator_delete,
            'dataset_collaborator_list': auth.dataset_collaborator_list,
        }

    # ITemplateHelpers
    def get_helpers(self):
        return {'collaborators_get_collaborators': get_collaborators}

    # IBlueprint
    def get_blueprint(self):
        return blueprint.collaborators_blueprint

