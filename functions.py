# a function for making settings common for all the axes in the main page
def axes_settings(axes):
    for ax in axes:
        # Remove the plot frame lines. They are unnecessary here.
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Ensure that the axis ticks only show up on the bottom and left of the plot.
        # Ticks on the right and top of the plot are generally unnecessary.
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # Provide tick lines across the plot to help your viewers trace along
        # the axis ticks. Make sure that the lines are light and small so they
        # don't obscure the primary data lines.
        ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        # Remove the tick marks; they are unnecessary with the tick lines we just
        # plotted.
        ax.tick_params(axis='both', which='both', bottom='off', top='off',
                        labelbottom='on', left='off', right='off', labelleft='on')

        # Label x- and y-axes
        ax.set_xlabel("Years", fontsize=16)
        ax.set_ylabel("Amount in millon NOK", fontsize=16)

    return axes
