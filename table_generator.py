# File: generate_table.py

from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, Tuple, List

def _draw_single_table(draw: ImageDraw.Draw, y_offset: int, instance_data: Dict, fonts: Dict):
    """Helper function to draw one complete table at a vertical offset."""
    
    results_data = instance_data['results_data']
    domain = instance_data['domain']
    initial_state = instance_data['initial_state']
    
    algorithms = list(results_data.keys())
    num_algorithms = len(algorithms)
    
    metrics_order = [
        "Solution Cost", "Solution Depth", "Nodes Generated", 
        "Nodes Expanded", "Max Frontier Size"
    ]
    
    # --- Configuration ---
    margin = 40
    title_height = 80
    row_height = 50
    metric_col_width = 240
    data_col_width = 200
    
    # Colors
    title_color = (10, 10, 10)
    header_color = (255, 255, 255)
    header_bg_color = (70, 130, 180)
    line_color = (200, 200, 200)
    text_color = (50, 50, 50)
    
    img_width = margin * 2 + metric_col_width + (num_algorithms * data_col_width)

    # --- Draw Title ---
    title_text = f"{domain} Performance Comparison"
    subtitle_text = f"Instance Start State: {initial_state}"
    
    title_bbox = draw.textbbox((0,0), title_text, font=fonts['title'])
    title_x = (img_width - (title_bbox[2] - title_bbox[0])) / 2
    draw.text((title_x, y_offset + 25), title_text, font=fonts['title'], fill=title_color)
    
    subtitle_bbox = draw.textbbox((0,0), subtitle_text, font=fonts['body'])
    subtitle_x = (img_width - (subtitle_bbox[2] - subtitle_bbox[0])) / 2
    draw.text((subtitle_x, y_offset + 65), subtitle_text, font=fonts['body'], fill=text_color)

    # --- Draw the Table ---
    table_y_start = y_offset + title_height + margin
    col_widths = [metric_col_width] + [data_col_width] * num_algorithms
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

def generate_combined_table_image(instance_results: List[Dict[str, Any]]):
    if not instance_results:
        print("No results data provided to generate table.")
        return

    # --- Calculate total image size ---
    num_instances = len(instance_results)
    first_results = instance_results[0]['results_data']
    num_algorithms = len(first_results.keys())

    margin = 40
    table_spacing = 30 
    metric_col_width = 240
    data_col_width = 200
    single_table_height = (80 + margin) + (6 * 50) # Title area + 6 rows
    
    img_width = margin * 2 + metric_col_width + (num_algorithms * data_col_width)
    img_height = (num_instances * (single_table_height + table_spacing)) - table_spacing + margin

    # --- Setup canvas and fonts ---
    bg_color = (245, 245, 245)
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
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

    # --- Draw each table ---
    for i, instance_data in enumerate(instance_results):
        y_offset = i * (single_table_height + table_spacing)
        _draw_single_table(draw, y_offset, instance_data, fonts)
        
    # --- Save Image ---
    output_filename = "performance_comparison_multiple.png"
    img.save(output_filename)
    print(f"\nCombined table image saved successfully as '{output_filename}'")
