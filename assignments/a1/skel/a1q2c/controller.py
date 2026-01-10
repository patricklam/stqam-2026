from . import settings

# The class that you are testing.
class Controller:
    def __init__(self, model):
        self.model = model

    def model_story(self):
        callee = getattr(self, f"model_story_{settings.WHICH_STORY}")
        return callee()

    def model_story_zero(self):
        self.model.wait()
        self.model.clear_resource()
        self.model.append_to_resource(17)
        self.model.append_to_resource(1729)
        self.model.append_to_resource("2025")
        x = []
        self.model.append_to_resource(x)
        rc = self.model.get_resource()
        self.model.signal()
        return rc

    # same as zero except missing the initial "wait()"
    def model_story_one(self):
        self.model.clear_resource()
        self.model.append_to_resource(17)
        self.model.append_to_resource(1729)
        self.model.append_to_resource("2025")
        x = []
        self.model.append_to_resource(x)
        rc = self.model.get_resource()
        self.model.signal()
        return rc

    # same as zero except only adds three items to the resource rather than four
    def model_story_two(self):
        self.model.wait()
        self.model.clear_resource()
        self.model.append_to_resource(17)
        self.model.append_to_resource(1729)
        self.model.append_to_resource("2025")
        rc = self.model.get_resource()
        self.model.signal()
        return rc

    # creates its own copy of the resource and returns that
    def model_story_three(self):
        self.model.clear_resource()
        self.model.append_to_resource(6)
        rc = self.model.get_resource()
        self.model.clear_resource()
        self.model.append_to_resource(5)
        rc = rc + self.model.get_resource()
        return rc

    # directly returns the model's resource
    def model_story_four(self):
        self.model.clear_resource()
        self.model.append_to_resource(6)
        rc = self.model.get_resource()
        self.model.clear_resource()
        self.model.append_to_resource(5)
        rc = rc + self.model.get_resource()
        return self.model.get_resource()

