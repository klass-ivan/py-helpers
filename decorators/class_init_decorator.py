__author__ = 'klass'


def inject_to_init(decorator_class, after, *mixin_args, **mixin_kwargs):
    """
        Parametrized class decorator that injects code before or after __init__
    """
    def class_decorator(target_class):
        orig_init = target_class.__init__

        def decorated_init(instance, *args, **kwargs):
            if not after:
                decorator_class(*mixin_args, **mixin_kwargs).decorate(instance)
            orig_init(instance, *args, **kwargs)
            if after:
                decorator_class(*mixin_args, **mixin_kwargs).decorate(instance)

        target_class.__init__ = decorated_init
        return target_class
    return class_decorator


class InitDecorator(object):
    """
        Base class. Extend it overriding your "decorate" method
    """

    @classmethod
    def before_init(cls, *args, **kwargs):
        return inject_to_init(cls, False, *args, **kwargs)

    @classmethod
    def after_init(cls, *args, **kwargs):
        return inject_to_init(cls, True, *args, **kwargs)

    def decorate(self, target_instance):
        """
            Does something with passed instance. Template method
        """
        pass