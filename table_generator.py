import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Tuple, List

def _draw_single_table(draw: ImageDraw.Draw, instance_data: Dict, fonts: Dict):
    """Helper function to draw one complete table on the provided canvas."""
    
    results_data = instance_data['results_data']
    domain = instance_data['domain']
    initial_state = instance_data['initial_state']
    
    algorithms = list(results_data.keys())
    
    metrics_order = [
        "Solution Cost", "Solution Depth", "Nodes Generated", 
        "Nodes Expanded", "Max Frontier Size"
    ]
    
    # --- Configuration ---
    margin = 40
    row_height = 50
    metric_col_width = 240
    data_col_width = 200
    
    # Colors
    title_color = (10, 10, 10)
    header_color = (255, 255, 255)
    header_bg_color = (70, 130, 180)
    line_color = (200, 200, 200)
    text_color = (50, 50, 50)
    
    img_width = margin * 2 + metric_col_width + (len(algorithms) * data_col_width)

    # --- Draw Title ---
    title_text = f"{domain} Performance Comparison"
    subtitle_text = f"Instance Start State: {initial_state}"
    
    title_bbox = draw.textbbox((0,0), title_text, font=fonts['title'])
    title_x = (img_width - (title_bbox[2] - title_bbox[0])) / 2
    draw.text((title_x, 25), title_text, font=fonts['title'], fill=title_color)
    
    subtitle_bbox = draw.textbbox((0,0), subtitle_text, font=fonts['body'])
    subtitle_x = (img_width - (subtitle_bbox[2] - subtitle_bbox[0])) / 2
    draw.text((subtitle_x, 65), subtitle_text, font=fonts['body'], fill=text_color)

    # --- Draw the Table ---
    table_y_start = 80 + margin
    col_widths = [metric_col_width] + [data_col_width] * len(algorithms)
    headers = ["Metric"] + algorithms

    # Header Row
    current_x = margin
    for i, header in enumerate(headers):
        draw.rectangle([current_x, table_y_start, current_x + col_widths[i], table_y_start + row_height], fill=header_bg_color)
        header_bbox = draw.textbbox((0,0), header, font=fonts['header'])
        text_w, text_h = header_bbox[2] - header_bbox[0], header_bbox[3] - header_bbox[1]
        text_pos = (current_x + (col_widths[i] - text_w) / 2, table_y_start + (row_height - text_h) / 2)
        draw.text(text_pos, header, font=fonts['header'], fill=header_color)
        current_x += col_widths[i]

    # Data Rows
    for i, metric in enumerate(metrics_order):
        row_y = table_y_start + (i + 1) * row_height
        draw.text((margin + 15, row_y + 15), metric, font=fonts['body'], fill=text_color)
        
        current_x = margin + col_widths[0]
        for j, algo in enumerate(algorithms):
            val = str(results_data[algo].get(metric, "N/A"))
            val_bbox = draw.textbbox((0,0), val, font=fonts['body'])
            val_w = val_bbox[2] - val_bbox[0]
            val_x = current_x + (col_widths[j+1] - val_w) / 2
            draw.text((val_x, row_y + 15), val, font=fonts['body'], fill=text_color)
            current_x += col_widths[j+1]

    # Grid Lines
    table_end_y = table_y_start + (len(metrics_order) + 1) * row_height
    table_end_x = margin + sum(col_widths)
    for i in range(len(metrics_order) + 2):
        y = table_y_start + i * row_height
        draw.line([(margin, y), (table_end_x, y)], fill=line_color, width=1)
    current_x = margin
    for width in col_widths:
        draw.line([(current_x, table_y_start), (current_x, table_end_y)], fill=line_color, width=1)
        current_x += width
    draw.line([(current_x, table_y_start), (current_x, table_end_y)], fill=line_color, width=1)

def generate_table_images(instance_results: List[Dict[str, Any]]):
    """
    Generates a separate image file for each instance's results and saves
    them in a 'table_results' directory.
    """
    if not instance_results:
        print("No results data provided to generate table.")
        return

    # --- Create output directory if it doesn't exist ---
    output_dir = "table_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: '{output_dir}'")
    
    # --- Load fonts once ---
    try:
        fonts = {
            'title': ImageFont.truetype("arialbd.ttf", 28),
            'header': ImageFont.truetype("arialbd.ttf", 18),
            'body': ImageFont.truetype("arial.ttf", 16)
        }
    except IOError:
        print("Arial font not found. Using default font.")
        fonts = {
            'title': ImageFont.load_default(),
            'header': ImageFont.load_default(),
            'body': ImageFont.load_default()
        }

    # --- Loop through each instance and create a separate image ---
    for i, instance_data in enumerate(instance_results):
        num_algorithms = len(instance_data['results_data'].keys())
        margin = 40
        metric_col_width = 240
        data_col_width = 200
        
        # Calculate dimensions for a single table image
        img_width = margin * 2 + metric_col_width + (num_algorithms * data_col_width)
        img_height = (80 + margin) + (6 * 50) + margin # Title area + 6 rows + bottom margin

        # Create canvas for this instance
        img = Image.new('RGB', (img_width, img_height), color=(245, 245, 245))
        draw = ImageDraw.Draw(img)
        
        # Draw the table content
        _draw_single_table(draw, instance_data, fonts)
        
        # Save the individual image file
        output_filename = f"performance_instance_{i+1}.png"
        full_path = os.path.join(output_dir, output_filename)
        img.save(full_path)
        print(f"  - Saved table for instance {i+1} to '{full_path}'")

    print(f"\nGenerated {len(instance_results)} table image(s) in the '{output_dir}' directory.")
