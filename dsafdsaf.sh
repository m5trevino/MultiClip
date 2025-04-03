#!/bin/bash
# Orchestrates unique blog content deployment to each domain

# --- Configuration ---
MARKDOWN_SOURCE_DIR="/home/flintx/bury/Peacock_Blog_Posts" # Directory where all your original markdown files live
ASTRO_PROJECT_ROOT="$(pwd)" # Current directory where this script lives
ASTRO_BLOG_CONTENT_DIR="$ASTRO_PROJECT_ROOT/src/content/blog" # Where Astro finds blog markdown files

# --- Domain and FTP Info ---
# Import the full list of domains and their credentials from your deploy script
# sourced_deploy_script is just a label, the script name is deploy_all_sites.sh
# We will read the credentials and domain lists from there
DEPLOY_SCRIPT="./deploy_all_sites.sh"


# --- File Distribution Mapping ---
# This associative array maps each domain's Htdocs path to a LIST of specific markdown file names
# (relative to MARKDOWN_SOURCE_DIR) that should be uploaded to that domain.
# You MUST customize this map for your desired distribution.
declare -A DOMAIN_FILE_MAP
DOMAIN_FILE_MAP=(
    # Example mappings - Replace with your actual desired distribution
    # Make sure the filenames match the ones in /home/flintx/bury/Peacock_Blog_Posts
    # Syntax: [domain/htdocs/path]="filename1.md filename2.md ..."
    ["4front.site/htdocs"]="blog_post_static_analysis_jadx.md blog_post_engineering_reliable_ai.md blog_post_control_your_digital_real_estate.md blog_post_diverse_background_tech_edge.md"
    ["getdome.pro/htdocs"]="blog_post_turning_chats_into_gold.md blog_post_diverse_background_tech_edge.md blog_post_static_analysis_jadx.md"
    ["trevino.today/htdocs"]="blog_post_control_your_digital_real_estate.md blog_post_static_analysis_jadx.md blog_post_engineering_reliable_ai.md"
    # Add mappings for ALL 25 of your domain_htdocs_paths here.
    # Ensure every domain you want content on is a key in this map.
    # You can include the same filename in multiple lists.
    ["blog.trevino.today/htdocs"]="blog_post_engineering_reliable_ai.md"
    ["matthew.trevino.today/htdocs"]="blog_post_turning_chats_into_gold.md"
    ["news.trevino.today/htdocs"]="blog_post_control_your_digital_real_estate.md"
    ["portfolio.trevino.today/htdocs"]="blog_post_philosophy_of_tools.md"
    ["resume.trevino.today/htdocs"]="blog_post_diverse_background_tech_edge.md"
    ["trevino-today.great-site.net/htdocs"]="blog_post_static_analysis_jadx.md"
    ["getdome.ct.ws/htdocs"]="blog_post_turning_chats_into_gold.md"
    ["logdog.getdome.pro/htdocs"]="blog_post_engineering_reliable_ai.md"
    ["matt.getdome.pro/htdocs"]="blog_post_control_your_digital_real_estate.md"
    ["matthew.getdome.pro/htdocs"]="blog_post_diverse_background_tech_edge.md"
    ["resume.getdome.pro/htdocs"]="blog_post_philosophy_of_tools.md"
    ["shop.getdome.pro/htdocs"]="blog_post_static_analysis_jadx.md"
    ["trevino.getdome.pro/htdocs"]="blog_post_turning_chats_into_gold.md"
    ["4front.42web.io/htdocs"]="blog_post_engineering_reliable_ai.md"
    ["blog.4front.site/htdocs"]="blog_post_diverse_background_tech_edge.md"
    ["matthewtrevino.4front.site/htdocs"]="blog_post_philosophy_of_tools.md"
    ["matttrevino.4front.site/htdocs"]="blog_post_static_analysis_jadx.md"
    ["news.4front.site/htdocs"]="blog_post_turning_chats_into_gold.md"
    ["portfolio.4front.site/htdocs"]="blog_post_engineering_reliable_ai.md"
    ["resources.4front.site/htdocs"]="blog_post_control_your_digital_real_estate.md"
    ["shop.4front.site/htdocs"]="blog_post_diverse_background_tech_edge.md"
    ["tabula.4front.site/htdocs"]="blog_post_philosophy_of_tools.md"
)


# --- Sanity Checks ---
if [ ! -d "$MARKDOWN_SOURCE_DIR" ]; then
  echo "[ERROR] Markdown source directory not found: $MARKDOWN_SOURCE_DIR"
  echo "Please ensure your source markdown files are in this location."
  exit 1
fi

if [ ! -f "$DEPLOY_SCRIPT" ]; then
  echo "[ERROR] Deploy script not found: $DEPLOY_SCRIPT"
  echo "Ensure this script is in the same directory as deploy_all_sites.sh."
  exit 1
fi

if [ ! -d "$ASTRO_BLOG_CONTENT_DIR" ]; then
  echo "[ERROR] Astro blog content directory not found: $ASTRO_BLOG_CONTENT_DIR"
  echo "Ensure your Astro project structure is correct (src/content/blog)."
  exit 1
fi

if [ ${#DOMAIN_FILE_MAP[@]} -eq 0 ]; then
    echo "[WARNING] DOMAIN_FILE_MAP is empty. No domains are configured for upload."
    echo "Please edit the script and configure DOMAIN_FILE_MAP."
    exit 0 # Exit gracefully if nothing to do
fi


# --- Main Orchestration Logic ---

echo "\n[INFO] Starting unique content deployment orchestration..."

# --- Step 1: Prepare initial Astro blog content dir ---
# Clear out the Astro blog content directory before starting
echo "[INFO] Clearing Astro blog content directory ($ASTRO_BLOG_CONTENT_DIR) for fresh content..."
rm -f "$ASTRO_BLOG_CONTENT_DIR"/*.md "$ASTRO_BLOG_CONTENT_DIR"/*.mdx # Remove existing blog posts

# --- Step 2: Process each domain ---
processed_domain_count=0
total_configured_domains=${#DOMAIN_FILE_MAP[@]}

# Source the deploy script to get access to FTP variables and domain lists defined within it
# WARNING: This executes the deploy script functions if not guarded!
# Assuming deploy_all_sites.sh has the variables defined at the top level
source "$DEPLOY_SCRIPT"

for DOMAIN_HTDOCS_PATH in "${!DOMAIN_FILE_MAP[@]}"; do
  processed_domain_count=$((processed_domain_count + 1))
  BLOG_FILES="${DOMAIN_FILE_MAP[$DOMAIN_HTDOCS_PATH]}"

  echo "\n[INFO] --- Processing Domain $processed_domain_count/$total_configured_domains: $DOMAIN_HTDOCS_PATH ---"

  # --- 2a: Populate Astro blog content dir with specific files for this domain ---
  echo "[INFO] Populating Astro blog content directory with files for $DOMAIN_HTDOCS_PATH..."
  current_files_copied=0
  for file_name in $BLOG_FILES; do
    SOURCE_FILE="$MARKDOWN_SOURCE_DIR/$file_name"
    DEST_FILE="$ASTRO_BLOG_CONTENT_DIR/$file_name"
    if [ -f "$SOURCE_FILE" ]; then
      cp "$SOURCE_FILE" "$DEST_FILE"
      current_files_copied=$((current_files_copied + 1))
      # echo "[INFO] Copied $file_name" # Too verbose
    else
      echo "[WARNING] Source file not found: $SOURCE_FILE. Skipping for this domain's build."
    fi
  done

  if [ $current_files_copied -eq 0 ]; then
    echo "[WARNING] No source files were successfully copied for $DOMAIN_HTDOCS_PATH. Skipping build and deploy for this domain."
    # Clean up the blog content directory again if no files were copied for this domain
    rm -f "$ASTRO_BLOG_CONTENT_DIR"/*.md "$ASTRO_BLOG_CONTENT_DIR"/*.mdx
    continue # Move to the next domain
  fi

  echo "[INFO] Copied $current_files_copied files to $ASTRO_BLOG_CONTENT_DIR."


  # --- 2b: Run Astro Build ---
  echo "[INFO] Running Astro build..."
  cd "$ASTRO_PROJECT_ROOT"
  npm run build || {
    echo "[ERROR] Astro build failed for content for $DOMAIN_HTDOCS_PATH. Check build logs."
    # Clean up the blog content directory again
    rm -f "$ASTRO_BLOG_CONTENT_DIR"/*.md "$ASTRO_BLOG_CONTENT_DIR"/*.mdx
    cd - > /dev/null # Go back to previous directory
    continue # Move to the next domain
  }
  echo "[SUCCESS] Astro build complete."


  # --- 2c: Deploy built content for this specific domain ---
  echo "[INFO] Starting deploy for $DOMAIN_HTDOCS_PATH..."

  # Find the correct FTP credentials from the sourced deploy script variables
  USER=""
  PASS=""
  HOST=""
  PORT=""

  # Need to parse the ALL_DOMAINS list from the sourced script
  # This is a bit manual but matches your script structure
  FOUND_FTP_INFO=false
  for item in "${ALL_DOMAINS[@]}"; do
      DOMAIN_IN_LIST=$(echo "$item" | cut -d: -f2)
      if [ "$DOMAIN_IN_LIST" == "$DOMAIN_HTDOCS_PATH" ]; then
          USER=$(echo "$item" | cut -d: -f3)
          PASS=$(echo "$item" | cut -d: -f4)
          HOST=$(echo "$item" | cut -d: -f5)
          PORT=$(echo "$item" | cut -d: -f6)
          FOUND_FTP_INFO=true
          break
      fi
  done

  if [ "$FOUND_FTP_INFO" = false ]; then
      echo "[ERROR] Could not find FTP info for $DOMAIN_HTDOCS_PATH in deploy script lists. Skipping deploy."
      # Clean up the blog content directory again
      rm -f "$ASTRO_BLOG_CONTENT_DIR"/*.md "$ASTRO_BLOG_CONTENT_DIR"/*.mdx
      continue # Move to the next domain
  fi


  # Use lftp to mirror the dist/ directory to the specific domain's htdocs
  # This mirrors the *entire* dist dir, which is fine since we only built the relevant content into it
  lftp -u "$USER","$PASS" -p "$PORT" "$HOST" <<EOF_LFTP
mirror -R --delete --verbose=3 ./dist/ "/$DOMAIN_HTDOCS_PATH/"
quit
EOF_LFTP

  if [ $? -eq 0 ]; then
    echo "[SUCCESS] Deploy finished for $DOMAIN_HTDOCS_PATH."
  else
    echo "[ERROR] Deploy failed for $DOMAIN_HTDOCS_PATH. Check lftp output."
  fi


  # --- 2d: Clean up Astro blog content directory for the next domain's content ---
  echo "[INFO] Cleaning Astro blog content directory ($ASTRO_BLOG_CONTENT_DIR) after deploy..."
  rm -f "$ASTRO_BLOG_CONTENT_DIR"/*.md "$ASTRO_BLOG_CONTENT_DIR"/*.mdx

done

echo "\n[INFO] --- Unique content deployment orchestration finished ---"