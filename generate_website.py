#!/usr/bin/env python3
# Copyright 2024 Ali Raheem
# MIT License
"""
Interactive shuffle visualization using Plotly.
Generates an HTML file with hover tooltips, suit filtering, and animation.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_and_transform_data(filename="blue.csv"):
    """Load CSV and transform to track each card's position through shuffles."""
    df = pd.read_csv(filename)

    # Get card names from initial state (column '1')
    cards = df['1'].tolist()
    num_shuffles = len(df.columns)

    # Build a mapping: for each shuffle column, map card -> position
    # Each column shows what card is at each position (1-indexed)
    card_positions = {card: [] for card in cards}

    for col_idx, col in enumerate(df.columns):
        for position, card in enumerate(df[col], start=1):
            card_positions[card].append(position)

    # Create long format DataFrame for Plotly
    records = []
    for card, positions in card_positions.items():
        suit = card[0]  # S, H, D, or C
        for shuffle_num, pos in enumerate(positions):
            records.append({
                'card': card,
                'suit': suit,
                'shuffle': shuffle_num,
                'position': pos
            })

    return pd.DataFrame(records), cards


def get_suit_color(suit):
    """Return color based on suit."""
    colors = {
        'H': '#E74C3C',  # Hearts - red
        'D': '#E74C3C',  # Diamonds - red
        'S': '#2C3E50',  # Spades - black
        'C': '#2C3E50',  # Clubs - black
    }
    return colors.get(suit, '#95A5A6')


def get_suit_name(suit):
    """Return full suit name."""
    names = {
        'H': 'Hearts',
        'D': 'Diamonds',
        'S': 'Spades',
        'C': 'Clubs',
    }
    return names.get(suit, 'Unknown')


def create_interactive_plot(df, cards):
    """Create the interactive Plotly visualization."""
    fig = go.Figure()

    suits = ['H', 'D', 'S', 'C']

    for suit in suits:
        suit_df = df[df['suit'] == suit]
        suit_color = get_suit_color(suit)
        suit_name = get_suit_name(suit)

        for card in suit_df['card'].unique():
            card_df = suit_df[suit_df['card'] == card].sort_values('shuffle')

            fig.add_trace(go.Scatter(
                x=card_df['shuffle'],
                y=card_df['position'],
                mode='lines+markers',
                name=suit_name,
                legendgroup=suit_name,
                showlegend=(card == suit_df['card'].unique()[0]),
                line=dict(color=suit_color, width=1.5),
                marker=dict(size=6),
                hovertemplate=(
                    '<b>%s</b><br>'
                    'Shuffle: %%{x}<br>'
                    'Position: %%{y}<extra></extra>'
                ) % card,
                customdata=[card] * len(card_df),
                visible=True,
            ))

    # Update layout
    fig.update_layout(
        title=dict(
            text='Card Positions Through 7 Riffle Shuffles',
            font=dict(size=20)
        ),
        xaxis=dict(
            title='Shuffle Number',
            tickmode='array',
            tickvals=list(range(8)),
            ticktext=['Initial', '1', '2', '3', '4', '5', '6', '7'],
            gridcolor='#E0E0E0',
        ),
        yaxis=dict(
            title='Position in Deck',
            autorange='reversed',
            dtick=5,
            gridcolor='#E0E0E0',
        ),
        hovermode='closest',
        plot_bgcolor='#F8F9FA',
        paper_bgcolor='white',
        height=800,
        width=1000,
        legend=dict(
            title='Suits',
            itemsizing='constant',
        ),
    )

    # Add dropdown for suit filtering
    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                direction='down',
                x=1.0,
                xanchor='left',
                y=1.15,
                yanchor='top',
                buttons=[
                    dict(
                        label='All Suits',
                        method='update',
                        args=[{'visible': [True] * len(fig.data)}],
                    ),
                    *[
                        dict(
                            label=get_suit_name(suit),
                            method='update',
                            args=[{
                                'visible': [
                                    trace.legendgroup == get_suit_name(suit)
                                    for trace in fig.data
                                ]
                            }]
                        )
                        for suit in suits
                    ]
                ]
            )
        ]
    )

    # Add animation buttons
    fig.update_layout(
        updatemenus=[
            *fig.layout.updatemenus,
            dict(
                type='buttons',
                direction='left',
                x=0.0,
                xanchor='left',
                y=1.15,
                yanchor='top',
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, {
                            'frame': {'duration': 500, 'redraw': True},
                            'fromcurrent': True,
                            'transition': {'duration': 300},
                        }]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0},
                        }]
                    ),
                ]
            )
        ]
    )

    # Create animation frames
    frames = []
    for shuffle_num in range(8):
        frame_data = []
        for trace in fig.data:
            card = trace.customdata[0]
            card_df = df[df['card'] == card].sort_values('shuffle')
            shuffle_df = card_df[card_df['shuffle'] <= shuffle_num]

            frame_data.append(go.Scatter(
                x=shuffle_df['shuffle'],
                y=shuffle_df['position'],
                mode='lines+markers',
                line=dict(color=trace.line.color, width=1.5),
                marker=dict(size=6),
            ))
        frames.append(go.Frame(data=frame_data, name=str(shuffle_num)))

    fig.frames = frames

    return fig


def main():
    """Main function to generate the interactive visualization."""
    print("Loading data...")
    df, cards = load_and_transform_data("blue.csv")

    print(f"Found {len(cards)} cards across {df['shuffle'].nunique()} shuffle states")

    print("Creating interactive plot...")
    fig = create_interactive_plot(df, cards)

    output_file = "shuffles_interactive.html"
    print(f"Saving to {output_file}...")
    fig.write_html(
        output_file,
        include_plotlyjs=True,
        full_html=True,
    )

    print(f"Done! Open {output_file} in your browser to view the visualization.")


if __name__ == "__main__":
    main()
