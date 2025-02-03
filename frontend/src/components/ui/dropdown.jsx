import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';
import {
  CheckIcon,
  ChevronRightIcon,
  DotFilledIcon,
} from '@radix-ui/react-icons';
import * as React from 'react';
import PropTypes from 'prop-types';

import { cn } from '@/utils/cn';

const DropdownMenu = DropdownMenuPrimitive.Root;

const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;

const DropdownMenuGroup = DropdownMenuPrimitive.Group;

const DropdownMenuPortal = DropdownMenuPrimitive.Portal;

const DropdownMenuSub = DropdownMenuPrimitive.Sub;

const DropdownMenuRadioGroup = DropdownMenuPrimitive.RadioGroup;

const DropdownMenuSubTriggerPropTypes = {
  className: PropTypes.string,
  inset: PropTypes.bool,
  children: PropTypes.node,
};

const DropdownMenuSubTrigger = React.forwardRef(({ className, inset, children, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.SubTrigger
      ref={ref}
      className={cn(
        'flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent data-[state=open]:bg-accent',
        inset && 'pl-8',
        className,
      )}
      {...props}
    >
      {children}
      <ChevronRightIcon className="ml-auto size-4" />
    </DropdownMenuPrimitive.SubTrigger>
  );
});

DropdownMenuSubTrigger.propTypes = DropdownMenuSubTriggerPropTypes;
DropdownMenuSubTrigger.displayName = DropdownMenuPrimitive.SubTrigger.displayName;

const DropdownMenuSubContentPropTypes = {
  className: PropTypes.string,
};

const DropdownMenuSubContent = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.SubContent
      ref={ref}
      className={cn(
        'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
        className,
      )}
      {...props}
    />
  );
});

DropdownMenuSubContent.propTypes = DropdownMenuSubContentPropTypes;
DropdownMenuSubContent.displayName = DropdownMenuPrimitive.SubContent.displayName;

const DropdownMenuContentPropTypes = {
  className: PropTypes.string,
  sideOffset: PropTypes.number,
};

const DropdownMenuContent = React.forwardRef(({ className, sideOffset = 4, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.Portal>
      <DropdownMenuPrimitive.Content
        ref={ref}
        sideOffset={sideOffset}
        className={cn(
          'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
          'data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className,
        )}
        {...props}
      />
    </DropdownMenuPrimitive.Portal>
  );
});

DropdownMenuContent.propTypes = DropdownMenuContentPropTypes;
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName;

const DropdownMenuItemPropTypes = {
  className: PropTypes.string,
  inset: PropTypes.bool,
};

const DropdownMenuItem = React.forwardRef(({ className, inset, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.Item
      ref={ref}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        inset && 'pl-8',
        className,
      )}
      {...props}
    />
  );
});

DropdownMenuItem.propTypes = DropdownMenuItemPropTypes;
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName;

const DropdownMenuCheckboxItemPropTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  checked: PropTypes.bool,
};

const DropdownMenuCheckboxItem = React.forwardRef(({ className, children, checked, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.CheckboxItem
      ref={ref}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className,
      )}
      checked={checked}
      {...props}
    >
      <span className="absolute left-2 flex size-3.5 items-center justify-center">
        <DropdownMenuPrimitive.ItemIndicator>
          <CheckIcon className="size-4" />
        </DropdownMenuPrimitive.ItemIndicator>
      </span>
      {children}
    </DropdownMenuPrimitive.CheckboxItem>
  );
});

DropdownMenuCheckboxItem.propTypes = DropdownMenuCheckboxItemPropTypes;
DropdownMenuCheckboxItem.displayName = DropdownMenuPrimitive.CheckboxItem.displayName;

const DropdownMenuRadioItemPropTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
};

const DropdownMenuRadioItem = React.forwardRef(({ className, children, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.RadioItem
      ref={ref}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className,
      )}
      {...props}
    >
      <span className="absolute left-2 flex size-3.5 items-center justify-center">
        <DropdownMenuPrimitive.ItemIndicator>
          <DotFilledIcon className="size-4 fill-current" />
        </DropdownMenuPrimitive.ItemIndicator>
      </span>
      {children}
    </DropdownMenuPrimitive.RadioItem>
  );
});

DropdownMenuRadioItem.propTypes = DropdownMenuRadioItemPropTypes;
DropdownMenuRadioItem.displayName = DropdownMenuPrimitive.RadioItem.displayName;

const DropdownMenuLabelPropTypes = {
  className: PropTypes.string,
  inset: PropTypes.bool,
};

const DropdownMenuLabel = React.forwardRef(({ className, inset, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.Label
      ref={ref}
      className={cn(
        'px-2 py-1.5 text-sm font-semibold',
        inset && 'pl-8',
        className,
      )}
      {...props}
    />
  );
});

DropdownMenuLabel.propTypes = DropdownMenuLabelPropTypes;
DropdownMenuLabel.displayName = DropdownMenuPrimitive.Label.displayName;

const DropdownMenuSeparatorPropTypes = {
  className: PropTypes.string,
};

const DropdownMenuSeparator = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <DropdownMenuPrimitive.Separator
      ref={ref}
      className={cn('-mx-1 my-1 h-px bg-muted', className)}
      {...props}
    />
  );
});

DropdownMenuSeparator.propTypes = DropdownMenuSeparatorPropTypes;
DropdownMenuSeparator.displayName = DropdownMenuPrimitive.Separator.displayName;

const DropdownMenuShortcutPropTypes = {
  className: PropTypes.string,
};

const DropdownMenuShortcut = ({ className, ...props }) => {
  return (
    <span
      className={cn('ml-auto text-xs tracking-widest opacity-60', className)}
      {...props}
    />
  );
};

DropdownMenuShortcut.propTypes = DropdownMenuShortcutPropTypes;
DropdownMenuShortcut.displayName = 'DropdownMenuShortcut';

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuRadioGroup,
};
