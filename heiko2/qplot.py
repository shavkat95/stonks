import torch
import inspect
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------

# @my_snooper.snoop()
def qplot(*args, where=None, styles=None, colors=None, limits=None, **kwargs):
    def get_variable_names(frame, args, kwargs):
        """Extract variable names from the caller's frame."""
        local_vars = frame.f_locals
        var_names = []
        for arg in args:
            found = False
            for name, val in local_vars.items():
                if val is arg:
                    var_names.append(name)
                    found = True
                    break
            if not found:
                var_names.append(f'var_{len(var_names)}')
        var_names += list(kwargs.keys())
        return var_names

    # Convert all PyTorch tensors to CPU
    args = [arg.cpu() if isinstance(arg, torch.Tensor) else arg for arg in args]
    kwargs = {k: v.cpu() if isinstance(v, torch.Tensor) else v for k, v in kwargs.items()}

    # Combine positional args and kwargs
    all_args = list(args) + list(kwargs.values())

    # Get variable names from the calling frame
    frame = inspect.currentframe().f_back
    var_names = get_variable_names(frame, args, kwargs)

    # Initialize parameters
    arrays = []
    if where is None:
        where = list(range(0, len(all_args)))  # Default where = [0, 1,..., n]

    if styles is None:
        styles = "-" * len(all_args)  # Default styles to all "-"

    # Default colors if not provided
    if colors is None:
        cmap = plt.get_cmap('tab20')
        colors = [cmap(i % 20) for i in range(30)]

    # Identify and separate arrays and highlight indices
    for i, arg in enumerate(all_args):
        if isinstance(arg, (list, np.ndarray, torch.Tensor, tuple)):
            arrays.append(arg)

    # Plotting
    unique_plots = sorted(set(where))
    num_plots = len(unique_plots)
    fig, axs = plt.subplots(num_plots, figsize=(10, 5 * num_plots), sharex=True)
    if num_plots == 1:
        axs = [axs]

    plot_titles = {idx: [] for idx in unique_plots}
    for i, array in enumerate(arrays):
        plot_idx = where[i % len(where)]  # Ensure the where index matches the number of arguments
        # Custom style "o": Scatterplot
        if styles[i % len(styles)] == 'o':
            axs[plot_idx].scatter(array, [arrays[plot_idx].flatten()[idx] for idx in array], color="r")
        # Custom style "a": Append
        elif styles[i % len(styles)] == 'a':
            if i > 0:
                prev_array = arrays[i - 1]
                # Plot the previous array
                axs[plot_idx].plot(range(len(prev_array)), prev_array, linestyle="-", color=colors[(i - 1) % len(colors)])
                # Connect the last point of the previous array with the first point of the current array
                axs[plot_idx].plot([len(prev_array) - 1, len(prev_array) - 1], [prev_array[-1], array[0]], linestyle="-", color=colors[(i - 1) % len(colors)])
                # Plot the current array starting from the same x-index as the last point of the previous array
                axs[plot_idx].plot(range(len(prev_array) - 1, len(prev_array) - 1 + len(array)), array, linestyle="-", color=colors[i % len(colors)])
            else:
                axs[plot_idx].plot(range(len(array)), array, linestyle="-", color=colors[i % len(colors)])
        else:
            # Plot tensor
            if isinstance(array, torch.Tensor):
                data = array.detach().squeeze()
                # Tensor with multiple dimensions
                if data.ndim > 1:
                    for y in range(array.size(0)):  # Number of subplots
                        axs[plot_idx].plot(array[y].squeeze(), linestyle=styles[i % len(styles)], color=colors[y % len(colors)])
                # Tensor with only 1 dimension (= vector)
                else:
                    axs[plot_idx].plot(data, linestyle=styles[i % len(styles)], color=colors[i % len(colors)])
            # Plot list / everything else
            else:
                axs[plot_idx].plot(array, linestyle=styles[i % len(styles)], color=colors[i % len(colors)])
        plot_titles[plot_idx].append(var_names[i % len(var_names)])

    for idx, title_vars in plot_titles.items():
        title = " and ".join(title_vars)  # Use title_vars directly to preserve order
        axs[idx].set_title(f'Variable(s) {title}')
        if limits:
            axs[idx].set_ylim(limits)

    if limits:
        for ax in axs:
            ax.set_ylim(limits)

    plt.tight_layout()
    plt.show()

qp = qplot

#--------------------------------------------------------------------------------------------

# qp (test1 = [1, 2, 3], test2 = [4, 5, 6], styles=["-", "a"], where=[0, 0], colors=["r", "b"])
