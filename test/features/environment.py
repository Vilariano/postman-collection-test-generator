from support.logger import *

def before_all(context):
    logging.info("Executing before all")

def after_all(context):
    logging.info("Executing after all")

def before_feature(context, feature):
    logging.info(f'Before feature: {feature} running...')

def after_feature(context, feature):
    logging.info(f'After Feature: {feature} running...')

def before_scenario(context, scenario):
    logging.info(f'Before scenario: {scenario} running...')
  
def after_scenario(context, scenario):
    logging.info(f'After scenario: {scenario} running...')

def before_step(context, step):
    logging.info(f'After before_step: {step} running...')

def after_step(context, step):
    logging.info(f'After step: {step} running...')
