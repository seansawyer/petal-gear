from typing import Any, Optional

import sdl2
import tcod.event

from actions import Action, MoveAction, QuitAction


class ControllerDeviceAdded(tcod.event.Event):
    """
    For more info on when this event is triggered see:
    https://wiki.libsdl.org/SDL_EventType#SDL_CONTROLLERDEVICEADDED

    Attributes:
        type (str): Always "CONTROLLERDEVICEADDED".
        which (int): The joystick device index of the added controller
    """

    def __init__(self, which: int):
        super().__init__()
        self.which = which

    @classmethod
    def from_sdl_event(cls, sdl_event: Any) -> "ControllerDeviceAdded":
        self = cls(sdl_event.cdevice.which)
        self.sdl_event = sdl_event
        return self

    def __repr__(self) -> str:
        return "tcod.event.%s(which=%d)" % (self.__class__.__name__, self.which)

    def __str__(self) -> str:
        return ("<%s, which=%d>") % (super().__str__().strip("<>"), self.which)


class ControllerDeviceRemoved(tcod.event.Event):
    """
    For more info on when this event is triggered see:
    https://wiki.libsdl.org/SDL_EventType#SDL_CONTROLLERDEVICEREMOVED

    Attributes:
        type (str): Always "CONTROLLERDEVICEREMOVED".
        which (int): The joystick device index of the removed controller
    """

    def __init__(self, which: int):
        super().__init__()
        self.which = which

    @classmethod
    def from_sdl_event(cls, sdl_event: Any) -> "ControllerDeviceRemoved":
        self = cls(sdl_event.cdevice.which)
        self.sdl_event = sdl_event
        return self

    def __repr__(self) -> str:
        return "tcod.event.%s(which=%d)" % (self.__class__.__name__, self.which)

    def __str__(self) -> str:
        return ("<%s, which=%d>") % (super().__str__().strip("<>"), self.which)


class ControllerAxisMotion(tcod.event.Event):

    def __init__(self, which: int, axis: int, value: int):
        super().__init__()
        self.which = which
        self.axis = axis  # SDL_GameControllerAxis value
        self.value = value  # -32768 <= value <= 32767

    @classmethod
    def from_sdl_event(cls, sdl_event: Any) -> "ControllerAxisMotion":
        self = cls(sdl_event.caxis.which, sdl_event.caxis.axis, sdl_event.caxis.value)
        self.sdl_event = sdl_event
        return self

    def __repr__(self) -> str:
        return "tcod.event.%s(which=%d, axis=%d, value=%d)" % (
            self.__class__.__name__, self.which, self.axis, self.value
        )

    def __str__(self) -> str:
        return ("<%s, which=%d, axis=%d, value=%d>") % (
            super().__str__().strip("<>"), self.which, self.axis, self.value
        )


class ControllerButtonDown(tcod.event.Event):

    def __init__(self, which: int, button: int):
        super().__init__()
        self.which = which
        self.button = button
        # TODO Should we also include `state` (SDL_PRESSED/SDL_RELEASED) here?
        # Or is that redundant?

    @classmethod
    def from_sdl_event(cls, sdl_event: Any) -> "ControllerButtonDown":
        self = cls(sdl_event.cbutton.which, sdl_event.cbutton.button)
        self.sdl_event = sdl_event
        return self

    def __repr__(self) -> str:
        return "tcod.event.%s(which=%d, button=self.button)" % (
            self.__class__.__name__, self.which, self.button
        )

    def __str__(self) -> str:
        return ("<%s, which=%d, button%d>") % (
            super().__str__().strip("<>"), self.which, self.button
        )


class ControllerButtonUp(tcod.event.Event):

    def __init__(self, which: int, button: int):
        super().__init__()
        self.which = which
        self.button = button  # SDL_GameControllerButton enum value
        # TODO Should we also include `state` (SDL_PRESSED/SDL_RELEASED) here?
        # Or is that redundant?

    @classmethod
    def from_sdl_event(cls, sdl_event: Any) -> "ControllerButtonUp":
        self = cls(sdl_event.cbutton.which, sdl_event.cbutton.button)
        self.sdl_event = sdl_event
        return self

    def __repr__(self) -> str:
        return "tcod.event.%s(which=%d)" % (self.__class__.__name__, self.which)

    def __str__(self) -> str:
        return ("<%s, which=%d>") % (super().__str__().strip("<>"), self.which)


class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self):
        self.controllers = {}

    def dispatch(self, event: Any) -> Optional[Action]:
        if isinstance(event, tcod.event.Undefined):
            return self.ev_undefined(event)
        return super().dispatch(event)

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        return QuitAction()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        if key == tcod.event.K_UP:
            action = MoveAction(0, -1)
        elif key == tcod.event.K_DOWN:
            action = MoveAction(0, 1)
        elif key == tcod.event.K_LEFT:
            action = MoveAction(-1, 0)
        elif key == tcod.event.K_RIGHT:
            action = MoveAction(1, 0)
        elif key == tcod.event.K_ESCAPE:
            action = QuitAction()
        return action

    def ev_controller_device_added(self, event: ControllerDeviceAdded) -> Optional[Action]:
        # `which` contains the joystick index of the added controller
        i = event.which
        assert i not in self.controllers
        controller = sdl2.SDL_GameControllerOpen(i)
        self.controllers[i] = controller
        print("Added controller {} {}".format(i, controller))
        return None

    def ev_controller_device_removed(self, event: ControllerDeviceRemoved) -> Optional[Action]:
        # `which` contains the joystick index of the removed controller
        i = event.which
        controller = self.controllers.get(i)
        if controller:
            print("Removed controller {} {}".format(i, controller, i))
            sdl2.SDL_GameControllerClose(controller)
            self.controllers.pop(i)
        return None

    def ev_controller_axis_motion(self, event: ControllerAxisMotion) -> Optional[Action]:
        i = event.which
        controller = self.controllers[i]
        print("Axis {} moved to {} on controller {} {}".format(
            event.axis, event.value, i, controller
        ))
        return None

    def ev_controller_button_down(self, event: ControllerButtonDown) -> Optional[Action]:
        i = event.which
        controller = self.controllers[i]
        print("Button {} down on controller {} {}".format(event.button, i, controller))
        action: Optional[Action] = None
        if event.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP:
            action = MoveAction(0, -1)
        elif event.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN:
            action = MoveAction(0, 1)
        elif event.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT:
            action = MoveAction(-1, 0)
        elif event.button == sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
            action = MoveAction(1, 0)
        return action

    def ev_controller_button_up(self, event: ControllerButtonUp) -> Optional[Action]:
        i = event.which
        controller = self.controllers[i]
        print("Button {} up on controller {} {}".format(event.button, i, controller))
        return None

    def ev_undefined(self, event: tcod.event.Undefined) -> Optional[Action]:
        # Controller device events
        if event.sdl_event.type == sdl2.SDL_CONTROLLERDEVICEADDED:
            new_event = ControllerDeviceAdded.from_sdl_event(event.sdl_event)
            return self.ev_controller_device_added(new_event)
        if event.sdl_event.type == sdl2.SDL_CONTROLLERDEVICEREMOVED:
            # only fires when an *open* controller is removed
            new_event = ControllerDeviceRemoved.from_sdl_event(event.sdl_event)
            return self.ev_controller_device_removed(new_event)
        # Controller axis events
        if event.sdl_event.type == sdl2.SDL_CONTROLLERAXISMOTION:
            new_event = ControllerAxisMotion.from_sdl_event(event.sdl_event)
            return self.ev_controller_axis_motion(new_event)
        # Controller button events
        if event.sdl_event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
            new_event = ControllerButtonDown.from_sdl_event(event.sdl_event)
            return self.ev_controller_button_down(new_event)
        if event.sdl_event.type == sdl2.SDL_CONTROLLERBUTTONUP:
            new_event = ControllerButtonUp.from_sdl_event(event.sdl_event)
            return self.ev_controller_button_up(new_event)
        return None
