# Appium Mobile App Test Automation

[한국어](./README.md) | **English**

[![Appium](https://img.shields.io/badge/Appium-663399?style=for-the-badge&logo=appium&logoColor=white)](https://appium.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

> E2E Test Automation for Woongjin Market Android App

---

## Project Overview

QA Engineer portfolio project implementing mobile test automation for a live production Android e-commerce app using Python + Appium.

### Key Features

| Feature | Description |
|---------|-------------|
| **Page Object Model** | 6 page classes for structured automation |
| **Image Validation** | Automatic broken image detection |
| **Auto Screenshot** | Screenshot + page source on failure |
| **Retry Logic** | Flaky test handling (pytest-rerunfailures) |
| **Logging System** | Centralized file + console logging |
| **Allure Report** | Visual test results |

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | Appium 2.x |
| Language | Python 3.11+ |
| Test Runner | Pytest 8.x |
| Reporting | Allure Report |
| Parallel | pytest-xdist |
| Retry | pytest-rerunfailures |

---

## Project Structure

```
woongjinAppTest/
├── src/
│   ├── config/
│   │   └── app_config.py          # App settings (driver, timeouts)
│   │
│   ├── pages/                     # Page Object Model
│   │   ├── base_page.py           # Common methods
│   │   ├── woongjin_app_home_page.py
│   │   ├── woongjin_app_category_page.py
│   │   ├── woongjin_app_search_page.py
│   │   ├── woongjin_app_login_page.py
│   │   ├── woongjin_app_like_page.py
│   │   └── woongjin_app_my_tab.py
│   │
│   ├── tests/                     # Test cases (10 files)
│   │   ├── test_home.py           # Home page (loading, scroll, images)
│   │   ├── test_category.py       # Category page
│   │   ├── test_search.py         # Search functionality
│   │   ├── test_login.py          # Login (positive)
│   │   ├── test_login_negative.py # Login (negative cases)
│   │   ├── test_my_tab.py         # My tab page
│   │   ├── test_gnb_tab.py        # GNB tab navigation
│   │   ├── test_navigation.py     # Full navigation integration
│   │   └── test_image_validation.py # Broken image detection
│   │
│   ├── utils/
│   │   ├── popup_handler.py       # Auto popup handling
│   │   ├── page_source_helper.py  # Page source analysis
│   │   ├── logger.py              # Logging system
│   │   └── exceptions.py          # Custom exceptions
│   │
│   └── conftest.py                # Pytest fixtures
│
├── docs/                          # Documentation
├── requirements.txt
└── pytest.ini
```

---

## Installation & Execution

```bash
# Clone repository
git clone https://github.com/YopleKiller/woongjinAppTest.git
cd woongjinAppTest

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start Appium server (separate terminal)
appium

# Run tests
pytest src/tests/ --reruns 1 -v
```

### Environment Variables (.env)

```env
APPIUM_SERVER_URL=http://127.0.0.1:4723
DEVICE_NAME=your_device_name
```

---

## Test Cases (10 files, 15+ tests)

| Test | Validation |
|------|------------|
| `test_home` | Home page loading, scroll, image verification |
| `test_category` | Category navigation, home return |
| `test_search` | Product search functionality |
| `test_login` | Positive login flow |
| `test_login_negative` | Login failure cases (wrong password, etc.) |
| `test_my_tab` | My tab access (logged in/out states) |
| `test_gnb_tab` | Individual GNB tab navigation |
| `test_navigation` | Full GNB traversal, rapid tab switching |
| `test_image_validation` | In-app broken image auto-detection |

---

## Key Implementations

### Page Object Model

```
BasePage (common: find_element, click, swipe, take_screenshot, find_broken_images)
  ├── WoongjinAppHomePage      Home screen
  ├── WoongjinAppCategoryPage  Categories
  ├── WoongjinAppSearchPage    Search
  ├── WoongjinAppLoginPage     Login
  ├── WoongjinAppLikePage      Favorites
  └── WoongjinAppMyTab         MY tab
```

### Broken Image Detection

```python
def test_check_broken_images(home_page):
    broken_images = home_page.find_broken_images()
    report_path, broken = home_page.save_broken_images_report("report.txt")
    assert len(broken_images) == 0, f"Found {len(broken_images)} broken images"
```

**Detection Logic:**
1. Traverse all `ImageView` elements
2. Flag as broken if width/height <= 1px
3. Collect resource-id, bounds info
4. Save report file

### Auto Popup Handling

```python
# utils/popup_handler.py
def handle_woongjin_popups(driver):
    """Auto-dismiss popups on app launch"""
```

---

## Auto Capture on Failure

Automatically saved on test failure:
- `screenshots/` - Screenshots
- `page_sources/` - Page source XML

---

## Lessons Learned

- **Appium**: Mobile app automation, element locator strategies (xpath, accessibility id, resource-id)
- **Image Validation**: Broken image detection logic, practical quality assurance
- **Stability**: Retry logic, popup handling to reduce flaky tests
- **Debugging**: Element discovery through page source analysis

---

## Related Projects

- [QATEST](https://github.com/yoplekiller/QATEST) - Python/Selenium Web + API Testing
- [PlaywrightQA](https://github.com/yoplekiller/PlaywrightQA) - TypeScript/Playwright Web Testing

---

## Author

**LIM JAE MIN**
- GitHub: [@YopleKiller](https://github.com/YopleKiller)
- Email: jmlim9244@gmail.com

---

## License

MIT License
