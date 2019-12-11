def config_frcnn_resnet_50_101(configs, config_params):
    print(config_params)
    model_config = configs['model']
    model_config.faster_rcnn.num_classes = config_params['num_classes']

    train_config = configs['train_config']

    train_config.batch_size = config_params['batch_size']
    train_config.optimizer.momentum_optimizer.learning_rate.manual_step_learning_rate.initial_learning_rate = config_params['learning_rate']
    
    if config_params['checkpoint_path'] is not None:
        train_config.fine_tune_checkpoint = config_params['checkpoint_path']

    return configs