# Testing Report

## Bug Findings
1. **Bug ID:** 001  
   **Description:** Application crashes when submitting a form without filling required fields.  
   **Steps to Reproduce:**  
   - Go to the form page.  
   - Leave required fields blank.  
   - Click 'Submit'.  
   **Expected Behavior:** No crash, display error message.

2. **Bug ID:** 002  
   **Description:** UI misalignment on mobile devices.  
   **Steps to Reproduce:**  
   - Open the app on a mobile device.  
   - Navigate to the main dashboard.  
   **Expected Behavior:** Proper alignment of UI components.

## Code Issues
- **Issue 1:** Deprecated API usage in `src/api.js` should be updated to the latest version.
- **Issue 2:** Code duplication found in `src/components/Button.js` and `src/components/SubmitButton.js` should be refactored.

## Improvement Suggestions
1. **Performance:** Optimize image loading by using lazy loading techniques.
2. **User Experience:** Add tooltips and helper text for form fields to enhance user guidance.